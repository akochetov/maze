from threading import Thread
from threading import Lock
from time import sleep
from misc.direction import Direction


class LineSensorThread(Thread):
    def __init__(self, source, frequency=10):
        """Thread to fetch line sensor data in given time intervals

        Arguments:
            source {LineSensorSourceBase} -- Instance of line sensor source
            to fetch data from

        Keyword Arguments:
            frequency {int} --  How many time per second signal
            has to be fetched from sensor (default: {10})
        """
        super().__init__()

        self.source = source
        self.frequency = frequency
        self.__state = None
        self.__directions = None
        self.__lock = Lock()

    def start(self):
        self.awake = True
        return super().start()

    def run(self):
        sleep_time = 1.0 / self.frequency
        while self.awake:
            self.update()
            sleep(sleep_time)

    def update(self):
        self.__lock.acquire()
        try:
            self.__state = self.source.get_state()
            self.__directions = self.source.get_directions()
        finally:
            self.__lock.release()

    def reset(self):
        self.source.reset()
        self.update()

    def exit(self):
        self.awake = False

    def get_state(self):
        self.__lock.acquire()
        try:
            return self.__state
        finally:
            self.__lock.release()

    def get_directions(self):
        self.__lock.acquire()
        try:
            return self.__directions
        finally:
            self.__lock.release()


class LineSensor(object):
    def __init__(self, source, frequency=10):
        """Line sensor implementation

        Arguments:
            source {LineSensorSourceBase} -- Source to fetch signals from

        Keyword Arguments:
            frequency {int} -- How many time per second signal
            has to be fetched from sensor (default: 10 times per second)
        """

        self.source = source
        self.thread = LineSensorThread(self.source, frequency)
        self.thread.start()

    def reset(self):
        self.thread.reset()

    def is_straight(self):
        return self.source.is_straight()

    def get_state(self):
        return self.thread.get_state()

    def get_directions(self):
        return self.thread.get_directions()

    def stop(self):
        if self.thread.is_alive():
            self.thread.exit()
            self.thread.join()

    def __del__(self):
        self.stop()
