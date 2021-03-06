from brains.brain_base import BrainBase
from brains.brain_base import ThinkThread
from misc.direction import Direction
from misc.log import log
from threading import Thread
from time import sleep
from time import time


class HandSearchBrain(BrainBase):
    def __init__(self, car, frequency, turn_bounce_time=0, lefthand=True):
        """Controls car movement with left-or-right hand search algorythm

        Arguments:
            frequency {float} -- number of state checks per second

        Keyword Arguments:
            turn_bounce_time {int} -- bounce time to avoid faulty turns
            (where car has to go fwd indeed) (default: {0})
            lefthand {bool} -- Is True, makes left hand search, otherwise
            right hand search (default: {True})
        """

        super().__init__(car, turn_bounce_time)

        self.thread = None
        self.lefthand = lefthand
        self.frequency = frequency

    def iterate(self, maze_map=None):
        return (
            self.left_hand_search()
            if self.lefthand else
            self.right_hand_search())

    def think(self, maze_map=None):
        """Finds the way out using left or right hand searches

        Arguments:
            car {Car} -- A Car to move around
            maze_map {MazeMap} -- MazeMap to navigate and make shortest path
        """

        self.maze_map = maze_map
        self.thread = ThinkThread(self, self.frequency)
        self.thread.start()

    def is_still_thinking(self):
        return self.thread is None or self.thread.awake

    def stop(self):
        if self.thread is not None:
            self.thread.exit()
            self.thread.join()

    def turn(self, cw):
        log('Brain says to turn clockwise: {}'.format(cw))
        self.car.stop()
        if cw:
            self.car.rotate_cw(stop_function=self.stop_function)
        else:
            self.car.rotate_ccw(stop_function=self.stop_function)
        self.update_turn_time()
        # disable brake at turns
        self.car.set_brake_status(False)
        log('Brain says: forward')
        self.car.move()

    def turn_around(self):
        log('Brain says: turn around')
        self.car.stop()
        self.car.turn_around(stop_function=self.stop_function)
        self.update_turn_time()
        # disable brake at turns
        self.car.set_brake_status(False)
        log('Brain says: forward')
        self.car.move()

    def hand_search(self, hand_direction):
        # get options where we can go
        dirs = self.car.sensors[0].get_directions()

        # None may mean end of the maze. Nothing to do here
        if dirs is None:
            log('Brain says: out!')
            return False

        # how long time ago we made a turn?
        # if too soon - don't do any checks now and just go fwd
        if not self.check_turn_bounce():
            return True

        # enable brake at turns
        self.car.set_brake_status(True)

        # is this a crossing? if so - remember it
        if self.maze_map is not None and self.check_crossing(dirs):
            self.maze_map.on_crossing(self.car)

        if len(dirs) == 0:
            dirs = [Direction.FORWARD]

        if len(dirs) == 1 and Direction.BACK in dirs:
            self.turn_around()
            return True

        if hand_direction in dirs:
            self.turn(hand_direction == Direction.RIGHT)
        else:
            if Direction.FORWARD in dirs:
                self.car.move()
            else:
                self.turn(hand_direction != Direction.RIGHT)

        return True

    def left_hand_search(self):
        return self.hand_search(Direction.LEFT)

    def right_hand_search(self):
        return self.hand_search(Direction.RIGHT)
