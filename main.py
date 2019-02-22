from signal import signal, SIGINT, SIGTERM
import sys
import os
import time
import random

from car import Car
from misc.orientation import Orientation
from misc.direction import Direction
from brains.maze_map import MazeMap
from brains.hand_search_brain import HandSearchBrain
from brains.path_brain import PathBrain
from sensors.line_sensor import LineSensor
import misc.settings as settings

# virtual imports
from worlds.virtual_world import VirtualWorld
from chassis.virtual_chassis import VirtualChassis
from sensors.virtual_line_sensor_source import VirtualLineSensorSource

ORIENTATION = Orientation.SOUTH

exit_loop = False


def exitLoop(arg1, arg2):
    global exit_loop
    exit_loop = True

signal(SIGINT, exitLoop)
signal(SIGTERM, exitLoop)

maze_world = None
chassis = None
line_sensor = None

if settings.VIRTUAL:
    # maze_file = 'maze20x20 - linefollow - large loop.txt'
    maze_file = 'maze10x10.txt'
    maze_world = VirtualWorld(maze_file)
    chassis = VirtualChassis(maze_world, settings.TIME_ERROR*1)
    line_sensor = LineSensor(
        VirtualLineSensorSource(maze_world, ORIENTATION),
        settings.CTRL_FREQ)
else:
    # physical RPi imports
    import RPi.GPIO as GPIO
    from worlds.line_world import LineWorld
    from chassis.rpi_2wheels_chassis import RPi2WheelsChassis
    from sensors.rpi_line_sensor_source import RPiLineSensorSource
    from misc.rpi_line_sensor_pid import RPiLineSensorPID

    GPIO.setmode(GPIO.BCM)

    maze_world = LineWorld()

    line_sensor = LineSensor(RPiLineSensorSource(
        settings.LINE_SENSORS,
        ORIENTATION,
        invert=True,
        signals_window_size=settings.SIGNALS_WINDOWS_SIZE,
        state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS
        ))

    sensor_pid = RPiLineSensorPID(
        settings.PID,
        line_sensor,
        settings.STATE_OK
    )

    chassis = RPi2WheelsChassis(
        settings.LEFT_MOTOR,
        settings.RIGHT_MOTOR,
        settings.LEFT_MOTOR_POWER,
        settings.RIGHT_MOTOR_POWER,
        settings.TIME_TO_TURN,
        settings.BRAKE_TIME,
        settings.PWM,
        sensor_pid,
        settings.PID_FREQ)

car = Car(maze_world, chassis, [line_sensor], ORIENTATION)
brain = HandSearchBrain(settings.CTRL_FREQ, lefthand=False)

maze_map = None
if settings.NAVIGATE_BACK:
    maze_map = MazeMap(car, settings.TIME_ERROR, settings.TIME_TO_TURN)

brain.think(car, maze_map)

while not exit_loop:
    if not brain.is_still_thinking():
        car.stop()

        if settings.NAVIGATE_BACK:
            maze_map.on_crossing(car)
            shortest_path = maze_map.get_shortest_path(reverse=True)
            print('Shortest path:')
            print(shortest_path)
            print()
            print('Full travelled map:')
            maze_map.save_full_path(sys.stdout)
            print()
            print('Going back. Current orient.: {}'.format(car.orientation))
            path_brain = PathBrain(shortest_path)

            # wait 5 seconds before returning back
            time.sleep(5)
            path_brain.think(car, maze_map=maze_map)
        break

    time.sleep(settings.TIME_ERROR*1)

    if settings.VIRTUAL:
        maze_world.save(sys.stdout)
        print()
        print()

print('Stopping brain, sensors and car.')

brain.stop()
car.stop()

print('All stopped.')

if not settings.VIRTUAL:
    GPIO.cleanup()
