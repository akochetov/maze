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

    def is_straight(self, state=None):
        return self.source.is_straight(
            self.get_state() if state is None else state)

    def is_turned(self, state=None):
        return self.source.is_turned(
            self.get_state() if state is None else state)

    def get_value(self, state=None):
        return self.source.get_value(
            self.get_state() if state is None else state)

    def get_state(self):
        return self.source.get_state()

    def get_directions(self):
        return self.source.get_directions()
