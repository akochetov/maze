from misc.direction import Direction


class LineSensor(object):
    LEFT = ["[1, 1, 0, 0, 0]", "[1, 1, 1, 0, 0]", "[1, 1, 0, 1, 1]"]
    RIGHT = ["[0, 0, 0, 1, 1]", "[0, 0, 1, 1, 1]", "[1, 1, 0, 1, 1]"]
    FORWARD = [
        "[1, 1, 1, 0, 0]",
        "[0, 0, 1, 1, 1]",
        "[0, 0, 1, 0, 0]",
        "[0, 1, 1, 1, 0]",
        "[0, 1, 1, 0, 0]",
        "[0, 0, 1, 1, 0]"]

    def __init__(self, source):
        """
        param source: instance of LineSensorSourceBase inherited class
        """
        self.source = source

    def __find_direction(self, state, direction):
        for dir in direction:
            if state == dir:
                return True

        return False

    def get_state(self):
        return self.source.get_state()

    def get_directions(self):
        ret = []
        state = str(self.get_state())

        if self.__find_direction(state, LineSensor.LEFT):
            ret.append(Direction.LEFT)

        if self.__find_direction(state, LineSensor.RIGHT):
            ret.append(Direction.RIGHT)

        if self.__find_direction(state, LineSensor.FORWARD):
            ret.append(Direction.FORWARD)

        return ret

    def is_crossing(self):
        dirs = self.get_directions()

        return\
            Direction.LEFT in dirs or\
            Direction.RIGHT in dirs or\
            len(dirs) == 0
