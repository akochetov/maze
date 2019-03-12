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
    line_sensor = LineSensor(VirtualLineSensorSource(maze_world, ORIENTATION))
else:
    # physical RPi imports
    import RPi.GPIO as GPIO
    from worlds.line_world import LineWorld
    from chassis.rpi_2wheels_chassis import RPi2WheelsChassis
    from sensors.rpi_line_sensor_source import RPiLineSensorSource
    from sensors.spi_line_sensor_source import SPiLineSensorSource
    from misc.rpi_line_sensor_pid import RPiLineSensorPID

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(settings.CTRL_LED, GPIO.OUT)
    GPIO.output(settings.CTRL_LED, GPIO.HIGH)

    GPIO.setup(settings.CTRL_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    maze_world = LineWorld()

    line_sensor_source = None
    if settings.SENSOR_TYPE == settings.SENSOR_SPI:
        line_sensor_source = SPiLineSensorSource(
        settings.SPI_LINE_SENSOR_CHANNELS,
        Orientation.SOUTH,
        settings.SPI_LINE_SENSOR_PARAMS["MIN"],
        settings.SPI_LINE_SENSOR_PARAMS["MID"],
        settings.SPI_LINE_SENSOR_PARAMS["MAX"],
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

maze_map = None
if settings.NAVIGATE_BACK:
    maze_map = MazeMap(car, settings.TIME_ERROR, settings.TIME_TO_TURN)

if not settings.VIRTUAL and len(sys.argv) <= 1:
    while (
        not exit_loop and
        GPIO.wait_for_edge(
            settings.CTRL_BTN,
            GPIO.FALLING,
            timeout=500) is None):
        pass

    GPIO.cleanup(settings.CTRL_BTN)

start_time = time.time()
brain.think(maze_map)

if not settings.VIRTUAL:
    GPIO.output(settings.CTRL_LED, GPIO.LOW)

while not exit_loop:
    if not brain.is_still_thinking():
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
            if path_brain.get_to_track():
                # now go back with shortest path
                path_brain.think(maze_map)
                # path_brain.get_to_track()
            else:
                print('Could NOT get back to line. Returning back stopped.')
        break

    time.sleep(settings.TIME_ERROR * 1)

    if settings.VIRTUAL:
        maze_world.save(sys.stdout)
        print()
        print()

print('Stopping brain, sensors and car.')

brain.stop()
car.stop()

print('All stopped.')

if not settings.VIRTUAL:
    GPIO.output(settings.CTRL_LED, GPIO.LOW)
    GPIO.cleanup()
