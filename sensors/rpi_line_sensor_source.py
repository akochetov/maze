from sensors.line_sensor_source_base import LineSensorSourceBase
from misc.direction import Direction
from misc.log import log
import RPi.GPIO as GPIO


class SignalStack(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.__current_size = 0
        self.__queue = [0] * self.max_size

    def put(self, item):
        if self.__current_size >= self.max_size:
            for i in range(0, self.max_size - 1):
                self.__queue[i] = self.__queue[i + 1]
            self.__current_size = self.max_size - 1
        try:
            self.__queue[self.__current_size] = item
            self.__current_size += 1
        except:
            log('current_size: {}'.format(self.__current_size))

    def get_items(self):
        return self.__queue[0:self.__current_size]

    def erase(self):
        self.__current_size = 0


class RPiLineSensorSource(LineSensorSourceBase):
    '''
    RPi implementation of digital line sensor with 5-7 IRs in line
    '''
    ALL = 0b11111
    LEFT = 0b10000
    RIGHT = 0b1
    FORWARD = 0b01110
    STRAIGHT = 0b00100
    OFF = 0

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
        self.signals_window_size = signals_window_size

        self.last_state = None
        self.out_reps = 0

        self.stack = SignalStack(signals_window_size)
        self.sensors = sensors
        self.invert = invert
        self.sensors_number = len(self.sensors)
        self.setup()

    def setup(self):
        for sensor in self.sensors:
            GPIO.setup(sensor, GPIO.IN)

        self.update_dirs()

    def update_dirs(self):
        self.LEFT = 1 << (self.sensors_number - 1)
        self.STRAIGHT = 0b1 << (self.sensors_number // 2)
        self.FORWARD = 0b111 << (self.sensors_number // 2 - 1)
        self.ALL = 0
        for i in range(0, self.sensors_number):
            self.ALL += 1 << i

    def reset(self):
        self.stack.erase()

    def is_straight(self, state):
        return state & self.STRAIGHT > 0

    def is_turned(self, state):
        return (
            state & self.LEFT > 0 or
            state & self.RIGHT)

    def get_state(self):
        ret = 0
        for i in range(0, self.sensors_number):
            inp = GPIO.input(self.sensors[i])
            if self.invert:
                ret += abs(inp - 1) << (self.sensors_number - i - 1)
            else:
                ret += inp << (self.sensors_number - i - 1)

        self.stack.put(ret)
        return ret

    def get_value(self, state):
        a, b = 0, 0
        for i in range(0, self.sensors_number):
            c = (state & (1 << i)) / (2 ** i)
            a += 1000 * c * i
            b += c

        if b == 0:
            b = 1

        return a / b

    def get_directions(self):
        ret = []
        state = self.get_state()

        # can we go FORWARD?
        if self.find_direction(state, self.FORWARD):
            ret.append(Direction.FORWARD)

        # are we OFF road?
        if (
            self.find_direction(state, self.OFF, True) or
            (
                self.find_direction(state, self.FORWARD) and
                not self.find_direction(state, self.LEFT) and
                not self.find_direction(state, self.RIGHT)
            )
        ):
            # we are OFF now, but we were just FWD (meaning we are to go BACK)
            if self.find_recent_direction(self.FORWARD):
                ret.append(Direction.BACK)

            # we are OFF or FWD now, but we just had crossing with LEFT turn
            if self.find_recent_direction(self.LEFT):
                ret.append(Direction.LEFT)

            # we are OFF or FWD now, but we just had crossing with RIGHT turn
            if self.find_recent_direction(self.RIGHT):
                ret.append(Direction.RIGHT)

        # if all prev are mainly ALL and we are still at ALL,
        # then maze way out found
        if (
            self.get_recent_direction_count(self.ALL, True) >=
            self.signals_window_size
        ):
            # Asumming that returning None means end of maze
            ret = None

        return ret

    def find_recent_direction(self, direction, exact_check=False):
        return (
            self.get_recent_direction_count(direction, exact_check) >=
            self.state_trigger_repetitions
            )

    def get_recent_direction_count(self, direction, exact_check=False):
        counter = 0
        for dir in self.stack.get_items():
            if self.find_direction(dir, direction, exact_check):
                counter += 1
        return counter

    def find_direction(self, state, direction, exact_check=False):
        if exact_check:
            return state == direction
        else:
            return state & direction > 0 or state == direction
