import sys
import os
import time
import random

'''
how to develop this further:
 * simplify task to line following. consider converting space to line
 following (?).
 * add configuration of a car step length, e.g. reasonable minimal distance
 unit car can cover as it moves forward.
 * later have a calibration, so step length can be converted to distance in cm.
 * have compass to add precision to car orientation.
 * add support of angle orientation.
 * configure orientation precision.
 * add orientation filter (actual compass value + aggregated calculated
 orientation).
 * add step coordinates calculation basing on distance and orientation
 per step.
 * build up a virtual maze map, map of moves: a list, first element is a
 source, then each subsequent - a structure of:
    is this step or turn.
    step length.
    step coordinates against S after move.
    orientation after move.
    reference to next list items.
    visit status. can be 1 and 2.
        1 means visited 1 or more times but still has children to move to
        2 means visited this step as well as all children.
        a node hat was visited and has only 1 child gets status 2 immediately
 * iteratively simplify map by joining steps with same orientation in one step.
 * when building map, know how to detect same node (closed loop), by comparing
 step coordinates with nodes already passed.
 * implement algorythm, where, if node was visited and no exit found - return
 back up until the node with status 1 is found.

HW:
 * compass
 * line following sensor
 * optical distance sensors (not immediately)
 * small powerbank

TODO:
 * add line follow support to a car
 * add motor support to a car
'''

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

virtual = True

if virtual:
    # maze_file = 'maze20x20 - linefollow - large loop.txt'
    maze_file = 'maze10x10.txt'
    maze_world = VirtualWorld(maze_file)
    chassis = VirtualChassis(maze_world, settings.TIME_ERROR*1)
    line_sensor = LineSensor(
        VirtualLineSensorSource(maze_world, ORIENTATION),
        state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS)
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

    maze_world = LineWorld(
        settings.STATE_OUT,
        settings.STATE_ACTION_REPETITIONS
        )

    line_sensor = LineSensor(
        RPiLineSensorSource(settings.LINE_SENSORS, ORIENTATION, invert=True),
        state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS
        )

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

        if virtual:
            maze_world.save(sys.stdout)

        print()
        print()
    except KeyboardInterrupt:
        print('Interrupted. Exiting.')
        brain.stop()
        car.stop()
        break

if not virtual:
    GPIO.cleanup()
