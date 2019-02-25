from brains.brain_base import BrainBase
from misc.direction import Direction
from time import sleep
from time import time


class PathBrain(BrainBase):
    '''Brain to be used to follow certain known path
    '''

    def __init__(self, car, path, frequency=10):
        self._car = car
        self._path = path
        self._thinking = False
        self._sleep_time = 1.0 / frequency

    def _check_crossing(self, dirs):
        """Returns True if car is on crossing

        Arguments:
            dirs {list of Direction} -- Directions car can go now

        Returns:
            [Boolean] -- True if car is on crossing and False otherwise
        """

        return (dirs is None or
                Direction.LEFT in dirs or
                Direction.RIGHT in dirs or
                Direction.BACK in dirs)

    def stop_function(self):
        """This function is used to know where to stop car
        when reversing from maze exit zone

        Returns:
            [Boolean] -- True if car has found a line and
            False if it hasn't yet
        """

        return self._car.sensors[0].get_directions() is not None

    def get_to_track(self):
        """Reveres from maze exit (black box) back to line

        Arguments:
            car {Car} -- car instance
        """

        self._car.move_to(Direction.BACK)
        start = time()
        enough_time = 1  # we give it 1 sec to reverse and find line
        while not stop_function() and time() - start < enough_time:
            sleep(1 / 100)
        return time() - start < enough_time

    def think(self, maze_map):
        """This returns car back with given algorythm (e.g. shortest path)

        Arguments:
            maze_map {MazeMap} -- maze map with visited nodes and route
        """

        self._thinking = True

        for node_id in self._path:
            direction = maze_map.navigate(
                self._path,
                node_id,
                self._car.orientation)

            if direction is None:
                break

            self._car.move_to(direction)
            # temporary implementation with printing moves out
            print('car.move({})'.format(direction))

            while True:
                dirs = self._car.sensors[0].get_directions()
                if self._check_crossing(dirs):
                    break
                sleep(self._sleep_time)

        self._thinking = False

    def is_still_thinking(self):
        return self._thinking
