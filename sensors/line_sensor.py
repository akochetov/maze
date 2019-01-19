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
        "[0, 0, 1, 1, 0]",
        "[0, 1, 0, 0, 0]",
        "[0, 0, 0, 1, 0]"]

    def __init__(self, source, state_trigger_repetitions=1):
        """[summary]

        Arguments:
            source {LineSensorSourceBase} -- instance of LineSensorSourceBase
            inherited class

        Keyword Arguments:
            state_trigger_repetitions {int} -- how many times state
            has to appear in signal in a row to count (default: {1})
        """
        self.source = source
        self.state_trigger_repetitions = state_trigger_repetitions
        self.trigger_repetitions = [0] * self.state_trigger_repetitions

    def __add_repetition(self, last_rep):
        for i in range(self.state_trigger_repetitions - 1):
            self.trigger_repetitions[i] = self.trigger_repetitions[i + 1]

        self.trigger_repetitions[self.state_trigger_repetitions - 1] = last_rep

    def __if_same_reps(self):
        first_rep = self.trigger_repetitions[0]
        for i in range(1, self.state_trigger_repetitions):
            if (self.trigger_repetitions[i] != first_rep):
                return False

        return True

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

        self.__add_repetition(state)

        if (
            self.__find_direction(state, LineSensor.LEFT) and
            self.__if_same_reps()
        ):
            ret.append(Direction.LEFT)

        if (
            self.__find_direction(state, LineSensor.RIGHT) and
            self.__if_same_reps()
        ):
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
