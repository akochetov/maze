from sensors.rpi_line_sensor_source import RPiLineSensorSource, SignalStack
from misc.log import log
import spidev


class SPiLineSensorSource(RPiLineSensorSource):
    '''
    SPi implementation of digital line sensor with 5-7 IRs in line
    working over SPI
    '''
    ALL = 0b1111111
    LEFT = 0b1110000
    RIGHT = 0b111
    FORWARD = 0b0011100
    STRAIGHT = 0b0001000
    OFF = 0

    # SPI bus params
    SPI_DEVICE = 0, 0
    SPI_SPEED = 1000000

    def __init__(
            self,
            sensors,
            orientation,
            sensors_min_max,
            invert=False,
            signals_window_size=10,
            state_trigger_repetitions=1
            ):
        super().__init__(
            sensors,
            orientation,
            invert,
            signals_window_size,
            state_trigger_repetitions)

        self.sensors_min_max = sensors_min_max

        # variable to store last read normalized (0..1 float per sensor) state
        self.float_state = [0] * self.sensors_number

    def setup(self):
        # open SPI bus
        self.spi = spidev.SpiDev()
        self.spi.open(*self.SPI_DEVICE)
        self.spi.max_speed_hz = self.SPI_SPEED

        # update direction values
        self.update_dirs()

    def update_dirs(self):
        pass

    def spi_read(self, channel):
        '''Read data from specific SPI channel

        Arguments:
            channel {int} -- SPI channel to read from

        Returns:
            [int] -- value read from SPI channel
        '''

        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def normalize(self, sensor_index, value):
        '''Converts SPI value to 0..1 calculated from max-min calibrated values

        Arguments:
            sensor_index {int} - which sensor has to be normalized basing
            on it's individual settings
            value {int} -- value read from SPI channel

        Returns:
            [float] -- value 0..1 calculated from max-min
            calibrated values and value read from SPI channel
        '''
        value_max = self.sensors_min_max[sensor_index]["MAX"]
        value_min = self.sensors_min_max[sensor_index]["MIN"]

        if value > value_max:
            return 0
            # value = value_max

        return (value_max - value) / (value_max - value_min)

    def input_binary(self, sensor_index, value):
        '''Converts SPI value to binary state, either 0 or 1

        Arguments:
            sensor_index {int} - which sensor has to be normalized basing
            on it's individual settings
            value {int} -- value read from SPI channel

        Returns:
            [int] - 1 if no line, 0 if there is a line
        '''
        return int(value > self.sensors_min_max[sensor_index]["MIN"])

    def get_state(self):
        ret = 0

        for i in range(0, self.sensors_number):
            # get value from SPI channel
            data = self.spi_read(self.sensors[i])
            self.float_state[i] = self.normalize(i, data)

            # convert it to binary output
            inp = self.input_binary(i, data)

            if self.invert:
                ret += abs(inp - 1) << i
            else:
                ret += inp << i

        self.stack.put(ret)
        return ret

    def is_straight(self, state):
        # return state & self.STRAIGHT > 0
        return state & self.FORWARD > 0

    def is_turned(self, state):
        return (
            state & self.LEFT > 0 or
            state & self.RIGHT)

    def get_value(self, state):
        a, b = 0, 0
        n = 4000.0 / (self.sensors_number - 1)
        for i in range(0, self.sensors_number):
            c = self.float_state[i]

            a += n * c * i
            b += c

        if b == 0:
            return 0

        return a / b

    def find_direction(self, state, direction, exact_check=False):
        if exact_check:
            return state == direction
        else:
            if direction in [self.LEFT, self.RIGHT]:
                return state & direction == direction or state == direction
            else:
                return state & direction > 0 or state == direction

