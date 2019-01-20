from misc.direction import Direction


class LineSensor(object):
    def __init__(self, source):
        """[summary]

        Arguments:
            source {LineSensorSourceBase} -- instance of LineSensorSourceBase
            inherited class

        Keyword Arguments:
            state_trigger_repetitions {int} -- how many times state
            has to appear in signal in a row to count (default: {1})
        """
        self.source = source

    def get_state(self):
        return self.source.get_state()

    def get_directions(self):
        return self.source.get_directions()

    def is_crossing(self):
        dirs = self.get_directions()

        return\
            Direction.LEFT in dirs or\
            Direction.RIGHT in dirs or\
            Direction.BACK in dirs  # len(dirs) == 0
