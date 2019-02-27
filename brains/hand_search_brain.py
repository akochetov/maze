from brains.brain_base import BrainBase
from misc.direction import Direction
from misc.log import log
from threading import Thread
from time import sleep
from time import time


class ThinkThread(Thread):
    def __init__(
            self,
            brain,
            frequency,
            lefthand
            ):
        super().__init__()

        self.brain = brain
        self.lefthand = lefthand
        self.sleep_time = 1.0 / frequency

    def start(self):
        self.awake = True
        return super().start()

    def run(self):
        while self.awake:
            sleep(self.sleep_time)

            if self.brain.car.is_out():
                self.awake = False
                break

            if self.awake:
                if self.lefthand:
                    if not self.brain.left_hand_search():
                        self.awake = False
                        break
                else:
                    if not self.brain.right_hand_search():
                        self.awake = False
                        break

    def exit(self):
        self.awake = False


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

        self.lefthand = lefthand
        self.frequency = frequency

    def think(self, maze_map=None):
        """Finds the way out using left or right hand searches

        Arguments:
            car {Car} -- A Car to move around
            maze_map {MazeMap} -- MazeMap to navigate and make shortest path
        """

        self.maze_map = maze_map
        self.thread = ThinkThread(self, self.frequency, self.lefthand)
        self.thread.start()

    def is_still_thinking(self):
        return self.thread.awake

    def stop(self):
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
        log('Brain says: forward')
        self.car.move()

    def turn_around(self):
        log('Brain says: turn around')
        self.car.stop()
        self.car.turn_around(stop_function=self.stop_function)
        self.update_turn_time()
        log('Brain says: forward')
        self.car.move()

    def hand_search(self, hand_direction):
        if not self.check_turn_bounce():
            return True

        if self.check_crossing(dirs):
            self.maze_map.on_crossing(self.car)

        if dirs is None:
            return False

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

    def left_hand_search(self, car):
        return self.hand_search(car, Direction.LEFT)

    def right_hand_search(self, car):
        return self.hand_search(car, Direction.RIGHT)
