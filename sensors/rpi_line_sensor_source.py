from sensors.line_sensor_source_base import LineSensorSourceBase
from misc.direction import Direction
from misc.log import log
import RPi.GPIO as GPIO


class SignalStack(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.__current_size = 0
        self.__queue = [] * self.max_size

    def put(self, item):
        if self.__current_size >= self.max_size:
            for i in range(0, self.__current_size - 1):
                self.__queue[i] = self.__queue[i + 1]
            self.__current_size = self.max_size - 1

        self.__queue[self.__current_size] = item
        self.__current_size += 1

    def get_items(self):
        return self.__queue[0:self.__current_size]

    def erase(self):
        self.__current_size = 0


class RPiLineSensorSource(LineSensorSourceBase):
    '''
    RPi implementation of digital line sensor with 5 IRs in line
    '''
    ALL = ["11111"]

    LEFT = [
        "11000",
        "11100",
        "11011",
        "10110",
        ALL]

    RIGHT = [
        "00011",
        "00111",
        "11011",
        "01101",
        ALL]

    FORWARD = [
        "11100",
        "11110",
        "00111",
        "01111",
        "00100",
        "01110",
        "01100",
        "00110",
        "01000",
        "00010",
        "11000",
        "00011",
        ALL]

    OFF = ["00000"]

    def __init__(
            self,
            sensors,
            orientation,
            invert=False,
            signals_window_size=10,
            state_trigger_repetitions=1
            ):
        super().__init__(orientation)

        self.state_trigger_repetitions = state_trigger_repetitions

        self.last_state = None
        self.out_reps = 0

        self.__stack = SignalStack(signals_window_size)
        self.__sensors = sensors
        self.__invert = invert
        self.__pins_number = len(self.__sensors)
        self.setup()

    def setup(self):
        for sensor in self.__sensors:
            GPIO.setup(sensor, GPIO.IN)

    def reset(self):
        self.__stack.erase()

    def get_state(self):
        ret = [0] * self.__pins_number
        for i in range(0, self.__pins_number):
            if self.__invert:
                ret[i] = abs(GPIO.input(self.__sensors[i]) - 1)
            else:
                ret[i] = GPIO.input(self.__sensors[i])

        self.__stack.put(ret)

        return super().bits_to_str(ret)

    def get_directions(self):
        ret = []
        state = self.get_state()

        # can we go FORWARD?
        if self.__find_direction(state, self.FORWARD):
            ret.append(Direction.FORWARD)

        # are we OFF road?
        if self.__find_direction(state, self.OFF):
            # we are OFF now, but we were just FWD (meaning we are to go BACK)
            if self.__find_recent_direction(self.FORWARD):
                ret.append(Direction.BACK)
            else:
                ret = []

        if Direction.OFF in ret or Direction.FORWARD in ret:
            # we are OFF or FWD now, but we just had crossing with LEFT turn
            if self.__find_recent_direction(self.LEFT):
                ret.append(Direction.LEFT)
            # we are OFF or FWD now, but we just had crossing with RIGHT turn
            if self.__find_recent_direction(self.RIGHT):
                ret.append(Direction.RIGHT)

        # if all prev are mainly ALL and we are still at ALL,
        # then maze way out found
        if (
            self.__get_recent_direction_count(self.ALL) >
            self.state_trigger_repetitions * 2
        ):
            # Asumming that returning None means end of maze
            ret = None

        return ret

    def __find_recent_direction(self, direction):
        return (
            self.__get_recent_direction_count(direction) >=
            self.state_trigger_repetitions
            )

    def __get_recent_direction_count(self, direction):
        counter = 0
        for dir in self.__stack.get_items():
            if dir in direction:
                counter += 1
        return counter

    def __find_direction(self, state, direction):
        if state is None:
            return False

        for dir in direction:
            if state == dir:
                return True

        return False
