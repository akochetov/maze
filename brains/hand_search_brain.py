from brains.brain_base import BrainBase
from misc.direction import Direction
from misc.log import log
from threading import Thread
from time import sleep


class ThinkThread(Thread):

    def __init__(self, car, maze_map, lefthand=True):
        super().__init__()

        self.car = car
        self.maze_map = maze_map
        self.lefthand = lefthand

    def start(self):
        self.awake = True
        return super().start()

    def run(self):
        while True:
            if not self.awake:
                break

            sleep(0.01/3)

            if self.car.is_out():
                self.awake = False
                break

            if self.maze_map is not None and self.car.sensors[0].is_crossing():
                # log('Crossing detected: {}'.format(
                #    self.car.sensors[0].get_state()
                #    ))
                self.maze_map.on_crossing(self.car)

            if self.lefthand:
                self.left_hand_search(self.car)
            else:
                self.right_hand_search(self.car)

    def exit(self):
        self.awake = False

    def stop_function(self):
        dirs = car.sensors[0].get_directions()

        return len(dirs) == 1 and Direction.FORWARD in dirs

    def left_hand_search(self, car):
        dirs = car.sensors[0].get_directions()

        if Direction.LEFT in dirs:
            car.stop()
            car.rotate_ccw(stop_function=self.stop_function)
            car.move(Direction.FORWARD)
        else:
            if Direction.FORWARD in dirs:
                car.move(Direction.FORWARD)
            else:
                car.stop()
                car.rotate_cw(stop_function=self.stop_function)
                car.move(Direction.FORWARD)

    def right_hand_search(self, car):
        dirs = car.sensors[0].get_directions()

        if Direction.RIGHT in dirs:
            car.stop()
            car.rotate_cw(stop_function=self.stop_function)
            car.move(Direction.FORWARD)
        else:
            if Direction.FORWARD in dirs:
                car.move(Direction.FORWARD)
            else:
                car.stop()
                car.rotate_ccw(stop_function=self.stop_function)
                car.move(Direction.FORWARD)


class HandSearchBrain(BrainBase):
    def __init__(self, lefthand=True):
        """Initiates a left-or-right hand search algorythm

        Keyword Arguments:
            lefthand {bool} -- Is True, makes left hand search, otherwise
            right hand search (default: {True})
        """
        self.lefthand = lefthand

    def think(self, car, maze_map=None):
        """Finds the way out using left or right hand searches

        Arguments:
            car {Car} -- A Car to move around
            maze_map {MazeMap} -- MazeMap to navigate and make shortest path
        """

        self.thread = ThinkThread(car, maze_map, self.lefthand)
        self.thread.start()

    def is_still_thinking(self):
        return self.thread.awake

    def stop(self):
        self.thread.exit()
        self.thread.join()
        pass
