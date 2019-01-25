from brains.brain_base import BrainBase
from misc.direction import Direction
from time import sleep


class PathBrain(BrainBase):
    '''Brain to be used to follow certain known path
    '''

    def __init__(self, path, frequency=10):
        self._path = path
        self._thinking = False
        self._sleep_time = 1.0 / frequency

    def _check_crossing(self, dirs):
        return (dirs is None or
                Direction.LEFT in dirs or
                Direction.RIGHT in dirs or
                Direction.BACK in dirs)

    def think(self, car, maze_map=None):
        self._thinking = True

        for node_id in self._path:
            direction = maze_map.navigate(self._path, node_id, car.orientation)

            if direction is None:
                break

            car.move_to(direction)
            # temporary implementation with printing moves out
            print('car.move({})'.format(direction))

            while True:
                dirs = car.sensors[0].get_directions()
                if self._check_crossing(dirs):
                    break
                sleep(self._sleep_time)

        self._thinking = False

    def is_still_thinking(self):
        return self._thinking
