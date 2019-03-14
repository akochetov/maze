from misc.direction import Direction
from time import time, sleep
from threading import Thread


class ThinkThread(Thread):
    def __init__(
            self,
            brain,
            frequency
            ):
        super().__init__()

        self.brain = brain
        self.sleep_time = 1.0 / frequency

    def start(self):
        self.awake = True
        return super().start()

    def stop(self):
        # we must be out. stop the car!
        self.brain.car.stop()
        self.awake = False

    def run(self):
        while self.awake:
            sleep(self.sleep_time)

            if self.brain.car.is_out():
                self.stop()
                break

            if self.awake and not self.brain.iterate():
                self.stop()
                break

    def exit(self):
        self.awake = False


class BrainBase(object):
    def __init__(self, car, turn_bounce_time=0):
        self.car = car
        self.turn_bounce_time = turn_bounce_time
        self.update_turn_time()

    def think(self, maze_map=None):
        pass

    def iterate(self):
        pass

    def is_still_thinking(self):
        pass

    def stop(self):
        pass

    def stop_function(self):
        """Function used to detect when it is time to finish turn.
        It basically checks if car is now on a straight line

        Returns:
            [Boolean] -- True if car is on straight line and
            turn has to be stopped
        """

        return self.car.sensors[0].is_straight()

    def check_crossing(self, dirs):
        """Returns True if car is on crossing

        Arguments:
            dirs {list of Direction} -- Directions car can go now

        Returns:
            [Boolean] -- True if car is on crossing and False otherwise
        """

        return (dirs is None or
                Direction.LEFT in dirs or
                Direction.RIGHT in dirs or
                (Direction.BACK in dirs and len(dirs) == 1))

    def check_turn_bounce(self):
        """Checks how long ago we turned. If it was too little time back,
        then we shall not turn and rather rely on PID to stablize car

        Returns:
            [Boolean] -- True if it is OK to turn or false if we just turned
            and so we have to cancel new turn
        """

        return (
            self.turn_bounce_time == 0 or
            time() - self.last_turn_time > self.turn_bounce_time
        )

    def update_turn_time(self):
        """Record time when we turned last time.
        Further used in turn bouncing checks
        """

        self.last_turn_time = time()
