from sensors.line_sensor_source_base import LineSensorSourceBase
from misc.direction import Direction
from misc.log import log
import RPi.GPIO as GPIO


class RPiLineSensorSource(LineSensorSourceBase):
    '''
    RPi implementation of digital line sensor with 5 IRs in line
    '''
    ALL = "[1, 1, 1, 1, 1]"

    LEFT = [
        "[1, 1, 0, 0, 0]",
        "[1, 1, 1, 0, 0]",
        "[1, 1, 0, 1, 1]",
        "[1, 0, 1, 1, 0]",
        ALL]

    RIGHT = [
        "[0, 0, 0, 1, 1]",
        "[0, 0, 1, 1, 1]",
        "[1, 1, 0, 1, 1]",
        "[0, 1, 1, 0, 1]",
        ALL]

    FORWARD = [
        "[1, 1, 1, 0, 0]",
        "[1, 1, 1, 1, 0]",
        "[0, 0, 1, 1, 1]",
        "[0, 1, 1, 1, 1]",
        "[0, 0, 1, 0, 0]",
        "[0, 1, 1, 1, 0]",
        "[0, 1, 1, 0, 0]",
        "[0, 0, 1, 1, 0]",
        "[0, 1, 0, 0, 0]",
        "[0, 0, 0, 1, 0]",
        "[1, 1, 0, 0, 0]",
        "[0, 0, 0, 1, 1]",
        ALL]

    OFF = ["[0, 0, 0, 0, 0]"]

    def __init__(
            self,
            sensors,
            orientation,
            invert=False,
            state_trigger_repetitions=1
            ):
        super().__init__(orientation)

        self.state_trigger_repetitions = state_trigger_repetitions
        self.trigger_repetitions = [0] * self.state_trigger_repetitions

        self.last_state = None
        self.out_reps = 0

        self.__sensors = sensors
        self.__invert = invert
        self._pins_number = len(self.__sensors)
        self.setup()

    def setup(self):
        for sensor in self.__sensors:
            GPIO.setup(sensor, GPIO.IN)

    def get_state(self):
        ret = [0]*self._pins_number
        for i in range(0, self._pins_number):
            if self.__invert:
                ret[i] = abs(GPIO.input(self.__sensors[i]) - 1)
            else:
                ret[i] = GPIO.input(self.__sensors[i])

        return ret

    def get_directions(self):
        ret = []
        state = str(self.get_state())

        # self.__add_repetition(state)

        if self.__find_direction(state, self.FORWARD):
            ret.append(Direction.FORWARD)

        # if all prev states were LEFT and now we are OFF or forward,
        # then we just passed LEFT turn
        if (
            self.__find_direction(self.last_state, self.LEFT) and
            self.__if_same_reps() and
            self.__passed_crossing(state)
        ):
            ret.append(Direction.LEFT)

        # if all prev states were RIGHT and now we are OFF or forward,
        # then we just passed RIGHT turn
        if (
            self.__find_direction(self.last_state, self.RIGHT) and
            self.__if_same_reps() and
            self.__passed_crossing(state)
        ):
            ret.append(Direction.RIGHT)

        # if we are off the track, but prev step was FORWARD,
        # then we have to turn back
        if (
            self.__find_direction(self.last_state, self.FORWARD) and
            self.__find_direction(state, self.OFF)
        ):
            ret.append(Direction.BACK)

        # if all prev are ALL and we are still at ALL,
        # then maze way out found
        if (
            self.__find_direction(self.last_state, [self.ALL]) and
            self.__find_direction(state, [self.ALL]) and
            self.__if_same_reps()
        ):
            self.out_reps += 1
            if self.out_reps >= self.state_trigger_repetitions:
                ret = None
            else:
                ret = []
            log(self.__dict__)
        else:
            self.out_reps = 0

        self.__add_repetition(state)

        return ret

    def reset(self):
        for i in range(self.state_trigger_repetitions):
            self.trigger_repetitions[i] = [""]

    def __add_repetition(self, last_rep):
        self.last_state = last_rep

        for i in range(self.state_trigger_repetitions - 1):
            self.trigger_repetitions[i] = self.trigger_repetitions[i + 1]

        self.trigger_repetitions[self.state_trigger_repetitions - 1] = last_rep

    def __if_same_reps(self):
        first_rep = self.trigger_repetitions[0]
        for i in range(1, self.state_trigger_repetitions):
            if (self.trigger_repetitions[i] != first_rep):
                return False

        return True

    def __passed_crossing(self, state):
        return (
            self.__find_direction(state, self.OFF) or
            self.__find_direction(state, self.FORWARD)
        )

    def __find_direction(self, state, direction):
        if state is None:
            return False

        for dir in direction:
            if state == dir:
                return True

        return False
