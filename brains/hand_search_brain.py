from brains.brain_base import BrainBase
from misc.direction import Direction
from misc.log import log
from threading import Thread
from time import sleep
from time import time


class ThinkThread(Thread):

    def __init__(self, car, maze_map, frequency, turn_bounce_time=0, lefthand=True):
        super().__init__()

        self.car = car
        self.maze_map = maze_map
        self.lefthand = lefthand
        self.turn_bounce_time = turn_bounce_time
        self.update_turn_time()
        self.sleep_time = 1.0 / frequency

    def start(self):
        self.awake = True
        return super().start()

    def run(self):
        while self.awake:
            sleep(self.sleep_time)

            if self.car.is_out():
                self.awake = False
                break

            if self.awake:
                if self.lefthand:
                    if not self.left_hand_search(self.car):
                        self.awake = False
                        break
                else:
                    if not self.right_hand_search(self.car):
                        self.awake = False
                        break

    def exit(self):
        self.awake = False

    def stop_function(self):
        # print('stop_function: {}'.format(
        #    bin(self.car.sensors[0].get_state())
        #    ))
        return self.car.sensors[0].is_straight()

    def _check_crossing(self, dirs):
        if (
            self.maze_map is not None and (
                dirs is None or
                Direction.LEFT in dirs or
                Direction.RIGHT in dirs or
                (Direction.BACK in dirs and len(dirs) == 1)
                )):
            self.maze_map.on_crossing(self.car)

    def ok_to_turn(self):
        return self.turn_bounce_time == 0 or time() - self.last_turn_time > self.turn_bounce_time

    def update_turn_time(self):
        self.last_turn_time = time()

    def hand_search(self, car, hand_direction):
        if not self.ok_to_turn():
            return True

        dirs = car.sensors[0].get_directions()
        self._check_crossing(dirs)

        if dirs is None:
            return False

        if len(dirs) == 0:
            # log('Ooops: {}'.format(car.sensors[0].source.__dict__))
            dirs = [Direction.FORWARD]

        if len(dirs) == 1 and Direction.BACK in dirs:
            log('Brain says: turn around: {}'.format(dirs))
            car.stop()
            car.turn_around(stop_function=self.stop_function)
            self.update_turn_time()
            log('Brain says: forward')
            car.move()
            return True

        if hand_direction in dirs:
            log('Brain says: right: {}'.format(dirs))
            car.stop()
            if hand_direction == Direction.RIGHT:
                car.rotate_cw(stop_function=self.stop_function)
            else:
                car.rotate_ccw(stop_function=self.stop_function)
            self.update_turn_time()
            log('Brain says: forward')
            car.move()
        else:
            if Direction.FORWARD in dirs:
                car.move()
            else:
                log('Brain says: left: {}'.format(dirs))
                car.stop()
                if hand_direction == Direction.RIGHT:
                    car.rotate_ccw(stop_function=self.stop_function)
                else:
                    car.rotate_cw(stop_function=self.stop_function)
                self.update_turn_time()
                log('Brain says: forward')
                car.move()
        return True

    def left_hand_search(self, car):
        return self.hand_search(car, Direction.LEFT)

    def right_hand_search(self, car):
        return self.hand_search(car, Direction.RIGHT)


class HandSearchBrain(BrainBase):
    def __init__(self, frequency, turn_bounce_time=0, lefthand=True):
        """Initiates a left-or-right hand search algorythm

        Keyword Arguments:
            lefthand {bool} -- Is True, makes left hand search, otherwise
            right hand search (default: {True})
        """
        self.lefthand = lefthand
        self.frequency = frequency
        self.turn_bounce_time = turn_bounce_time

    def think(self, car, maze_map=None):
        """Finds the way out using left or right hand searches

        Arguments:
            car {Car} -- A Car to move around
            maze_map {MazeMap} -- MazeMap to navigate and make shortest path
        """

        self.thread = ThinkThread(car, maze_map, self.frequency, self.turn_bounce_time, self.lefthand)
        self.thread.start()

    def is_still_thinking(self):
        return self.thread.awake

    def stop(self):
        self.thread.exit()
        self.thread.join()
        pass
