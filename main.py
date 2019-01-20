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

if settings.VIRTUAL:
    # maze_file = 'maze20x20 - linefollow - large loop.txt'
    maze_file = 'maze10x10.txt'
    maze_world = VirtualWorld(maze_file)
    chassis = VirtualChassis(maze_world, settings.TIME_ERROR*1)
    line_sensor = LineSensor(VirtualLineSensorSource(maze_world, ORIENTATION))
    car = Car(maze_world, chassis, [line_sensor], ORIENTATION)
    maze_map = MazeMap(car, settings.TIME_ERROR, settings.TIME_TO_TURN)
    brain = HandSearchBrain(lefthand=True)
else:
    # physical RPi imports
    import RPi.GPIO as GPIO
    from worlds.line_world import LineWorld
    from chassis.rpi_2wheels_chassis import RPi2WheelsChassis
    from sensors.rpi_line_sensor_source import RPiLineSensorSource
    from misc.rpi_line_sensor_pid import RPiLineSensorPID
    from misc.state_action import StateAction

    GPIO.setmode(GPIO.BCM)

    maze_world = LineWorld()

    line_sensor = LineSensor(RPiLineSensorSource(
        settings.LINE_SENSORS,
        ORIENTATION,
        invert=True,
        state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS
        ))

    state_action = StateAction(settings.STATE_ERROR, settings.STATE_ACTION)

    sensor_pid = RPiLineSensorPID(
        settings.PID,
        line_sensor,
        state_action,
        settings.STATE_OK
    )

    chassis = RPi2WheelsChassis(
        settings.LEFT_MOTOR,
        settings.RIGHT_MOTOR,
        settings.LEFT_MOTOR_POWER,
        settings.RIGHT_MOTOR_POWER,
        settings.TIME_TO_TURN,
        settings.PWM,
        sensor_pid,
        settings.FREQ)

    car = Car(maze_world, chassis, [line_sensor], ORIENTATION)
    maze_map = MazeMap(car, settings.TIME_ERROR, settings.TIME_TO_TURN)
    brain = HandSearchBrain(lefthand=False)

brain.think(car, maze_map)

while True:
    try:
        if not brain.is_still_thinking():
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
            path_brain.think(car, maze_map=maze_map)
            break

        time.sleep(settings.TIME_ERROR*1)

        if settings.VIRTUAL:
            maze_world.save(sys.stdout)

        print()
        print()
    except KeyboardInterrupt:
        print('Interrupted. Exiting.')
        brain.stop()
        car.stop()
        break

if not settings.VIRTUAL:
    GPIO.cleanup()
