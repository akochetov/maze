from signal import signal, SIGINT, SIGTERM, SIGUSR1
from subprocess import check_call
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
time_to_go = False


def exitLoop(arg1, arg2):
    global exit_loop
    exit_loop = True


def go(arg1, arg2):
    global time_to_go
    time_to_go = True

# setup signals to stop program properly when interrupted by user
signal(SIGINT, exitLoop)
signal(SIGTERM, exitLoop)
# setup signal to launch car at button press
signal(SIGUSR1, go)
# raise prio of process
check_call('sudo renice -n -20 {}'.format(os.getpid()), shell=True)


maze_world = None
chassis = None
line_sensor = None

if settings.VIRTUAL:
    # maze_file = 'maze20x20 - linefollow - large loop.txt'
    maze_file = 'maze10x10.txt'
    maze_world = VirtualWorld(maze_file)
    chassis = VirtualChassis(maze_world, settings.TIME_ERROR*1)
    line_sensor = LineSensor(VirtualLineSensorSource(maze_world, ORIENTATION))
else:
    # physical RPi imports
    import RPi.GPIO as GPIO
    from worlds.line_world import LineWorld
    from chassis.rpi_2wheels_chassis import RPi2WheelsChassis
    from sensors.rpi_line_sensor_source import RPiLineSensorSource
    from sensors.spi_line_sensor_source import SPiLineSensorSource
    from misc.rpi_line_sensor_pid import RPiLineSensorPID

    maze_world = LineWorld()

    line_sensor_source = None
    if settings.SENSOR_TYPE == settings.SENSOR_SPI:
        line_sensor_source = SPiLineSensorSource(
            settings.SPI_LINE_SENSOR_CHANNELS,
            Orientation.SOUTH,
            settings.SPI_LINE_SENSOR_MIN_MAX,
            invert=True,
            signals_window_size=settings.SIGNALS_WINDOWS_SIZE,
            state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS
            )

    if settings.SENSOR_TYPE == settings.SENSOR_GPIO:
        line_sensor_source = RPiLineSensorSource(
            settings.LINE_SENSORS,
            ORIENTATION,
            invert=True,
            signals_window_size=settings.SIGNALS_WINDOWS_SIZE,
            state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS
            )

    line_sensor = LineSensor(line_sensor_source)

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
brain = HandSearchBrain(
    car,
    settings.CTRL_FREQ,
    turn_bounce_time=settings.TURN_BOUNCE_TIME,
    lefthand=False
    )

path_brain = None
maze_map = None
if settings.NAVIGATE_BACK:
    maze_map = MazeMap(car, settings.TIME_ERROR, settings.TIME_TO_TURN)

if not settings.VIRTUAL and len(sys.argv) <= 1:
    # wait for button to be pressed again to start a car
    while not exit_loop and not time_to_go:
        pass

start_time = time.time()
brain.think(maze_map)

while not exit_loop:
    if not brain.is_still_thinking() and path_brain is None:
        print('Maze time: {}'.format(time.time()-start_time))
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

            path_brain = PathBrain(
                car,
                shortest_path,
                settings.CTRL_FREQ,
                turn_bounce_time=settings.TURN_BOUNCE_TIME
                )

            # wait a few seconds before returning back
            time.sleep(3)
            # reverse and get to the line
            path_brain.get_to_track()
            # now go back with shortest path
            path_brain.think(maze_map)
        else:
            # finish straight away since there is no navigation back
            break

    if path_brain is not None and not path_brain.is_still_thinking():
        # we got back - exit now
        break

    time.sleep(settings.TIME_ERROR)

    if settings.VIRTUAL:
        maze_world.save(sys.stdout)
        print()
        print()

print('Stopping brain, sensors and car.')

if path_brain is not None:
    path_brain.stop()
brain.stop()
car.stop()

print('All stopped.')
