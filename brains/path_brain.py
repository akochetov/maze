from brains.brain_base import BrainBase
from brains.brain_base import ThinkThread
from misc.direction import Direction
from time import sleep
from time import time


class PathBrain(BrainBase):
    '''Brain to be used to follow certain known path
    '''

    def __init__(self, car, path, frequency, turn_bounce_time=0):
        super().__init__(car, turn_bounce_time)

        self.path = path
        self.thread = None
        self.frequency = frequency
        self.current_node = None

    def return_stop_function(self):
        """This function is used to know where to stop car
        when reversing from maze exit zone

        Returns:
            [Boolean] -- True if car has found a line and
            False if it hasn't yet
        """
        # return True when car detects the line
        # (directions to move left, right or fwd)
        return self.car.sensors[0].get_directions() is not None

    def get_to_track(self):
        """Reveres from maze exit (black box) back to line

        Arguments:
            car {Car} -- car instance
        """

        self.car.move_to(Direction.BACK)
        start = time()
        enough_time = 1  # we give it 1 sec to reverse and find line max
        while not self.return_stop_function() and time() - start < enough_time:
            pass
        self.car.stop(False)
        return time() - start < enough_time

    def iterate(self, maze_map=None):
        # now navigate
        if self.current_node is None:
            self.current_node = self.path[0]
        else:
            ind = self.path.find(self.current_node)
            # last node in path - stop
            if ind == len(self.path) - 1:
                self.car.move_to(Direction.BACK, self.stop_function)
                return False
            self.current_node = self.path[ind + 1]

        # is it crossing?
        dirs = self.car.sensors[0].get_directions()
        ok_to_turn = self.check_turn_bounce()
        self.car.set_brake_status(ok_to_turn)

        if self.check_crossing(dirs) and ok_to_turn:
            direction = maze_map.navigate(
                self.path,
                self.current_node,
                self.car.orientation)

            # if we finished full path?
            if direction is None:
                return False

            self.car.move_to(direction, self.stop_function)
            self.update_turn_time()
            # disable brake at turns
            self.car.set_brake_status(False)

            # temporary implementation with printing moves out
            print('car.move({})'.format(direction))

    def think(self, maze_map):
        """This returns car back with given algorythm (e.g. shortest path)

        Arguments:
            maze_map {MazeMap} -- maze map with visited nodes and route
        """

        # slightly move car forward so it gets straight
        # on the line thanks to PID.
        # This is to avoid situation when car is back on the line
        # at an angle and so it interprets it as a first turn on
        # the way back (mistakenly)
        self.car.move_to(Direction.FORWARD)
        self.update_turn_time()
        # disable brake at turns
        self.car.set_brake_status(False)
        sleep(0.5)
        self.car.stop(False)

        self.maze_map = maze_map
        self.thread = ThinkThread(self, self.frequency)
        self.thread.start()

    def is_still_thinking(self):
        return self.thread is None or self.thread.awake

    def stop(self):
        if self.thread is not None:
            self.thread.exit()
            self.thread.join()
