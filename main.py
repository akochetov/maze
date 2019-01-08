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
 
TODO:
 * develop line follow virtual sensor class
 * develop line follow HW class
 * add line follow support to a car
 * add motor virtual class
 * add motor HW class
 * add motor support to a car
 * add config for everything. make it py file this time
 * make sure sensors only work from maze state
'''


from worlds.virtual_world import VirtualWorld
from car import Car
from brains.orientation import Orientation
from brains.direction import Direction
from brains.maze_map import MazeMap
from chassis.virtual_chassis import VirtualChassis
from brains.hand_search_brain import HandSearchBrain

maze_file = 'maze20x20 - linefollow - large loop.txt'
maze_world = VirtualWorld(maze_file)
chassis = VirtualChassis(maze_world, 0.5)
car = Car(maze_world, chassis, Orientation.SOUTH)
maze_map = MazeMap(car)
brain = HandSearchBrain()
    
brain.think(car)

for i in range(0,1000):
    if not brain.is_still_thinking():
        print(maze_map.get_shortest_path())
        break

    time.sleep(0.5)
    maze_world.save(sys.stdout)
    print()
    print()






