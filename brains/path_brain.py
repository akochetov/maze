from brains.brain_base import BrainBase
from misc.direction import Direction


class PathBrain(BrainBase):
    '''Brain to be used to follow certain known path
    '''

    def __init__(self, path):
        self._path = path
        self._thinking = False

    def think(self, car, maze_map=None):
        self._thinking = True

        for node_id in self._path:
            direction = maze_map.navigate(self._path, node_id, car.orientation)

            if direction is None:
                break

            car.move(direction)
            # temporary implementation with printing moves out
            print('car.move({})'.format(direction))

        self._thinking = False

    def is_still_thinking(self):
        return self._thinking
