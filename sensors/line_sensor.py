from threading import Thread
from threading import Lock
from time import sleep
from misc.direction import Direction


class LineSensor(object):
    def __init__(self, source):
        """Line sensor implementation

        Arguments:
            source {LineSensorSourceBase} -- Source to fetch signals from
        """

        self.source = source

    def reset(self):
        self.source.reset()

    def is_straight(self):
        return self.source.is_straight()

    def is_turned(self):
        return self.source.is_turned()

    def get_value(self):
        return self.source.get_value()

    def get_state(self):
        return self.source.get_state()

    def get_directions(self):
        return self.source.get_directions()
