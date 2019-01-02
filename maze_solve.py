import sys
import os
import time
import random

'''
how to develop this further:
 * simplify task to line following. consider converting space to line following (?).
 * add configuration of a car step length, e.g. reasonable minimal distance unit car can cover as it moves forward.
 * later have a calibration, so step length can be converted to distance in cm.
 * have compass to add precision to car orientation.
 * add support of angle orientation.
 * configure orientation precision.
 * add orientation filter (actual compass value + aggregated calculated orientation).
 * add step coordinates calculation basing on distance and orientation per step.
 * build up a virtual maze map, map of moves: a list, first element is a source, then each subsequent - a structure of:
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
 * when building map, know how to detect same node (closed loop), by comparing step coordinates with nodes already passed.
 * implement algorythm, where, if node was visited and no exit found - return back up until the node with status 1 is found.

HW:
 * compass
 * line following sensor
 * optical distance sensors (not immediately)
 * small powerbank
'''


from maze_state import MazeState
from car import Car
from orientation import Orientation
from direction import Direction
from maze_map import MazeMap

maze_file = 'maze10x10.txt'
maze_state = MazeState(maze_file)
car = Car(maze_state, Orientation.SOUTH)
maze_map = MazeMap(car)

def left_hand_search():
    if car.sensors[0].get_distance():
        car.move(Direction.LEFT)
    else:
        if car.sensors[1].get_distance():
            car.move(Direction.FORWARD)
        else:
            car.move(Direction.RIGHT)

def right_hand_search():
    if car.sensors[2].get_distance():
        car.move(Direction.RIGHT)
    else:
        if car.sensors[1].get_distance():
            car.move(Direction.FORWARD)
        else:
            car.move(Direction.LEFT)

for i in range(0,1000):
    time.sleep(0.1)
    maze_state.save(sys.stdout)

    if car.is_out():
        print(maze_map.get_shortest_path())
        exit()

    left_hand_search()
    #right_hand_search()

    print()
    print()




