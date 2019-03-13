from sensors.rpi_line_sensor_source import RPiLineSensorSource, SignalStack
from misc.log import log
import spidev


class SPiLineSensorSource(RPiLineSensorSource):
    '''
    SPi implementation of digital line sensor with 5-7 IRs in line
    working over SPI
    '''
    ALL = 0b11111
    LEFT = 0b10000
    RIGHT = 0b1
    FORWARD = 0b01110
    STRAIGHT = 0b00100
    OFF = 0

    # SPI bus params
    SPI_DEVICE = 0, 0
    SPI_SPEED = 1000000

    def __init__(
            self,
            sensors,
            orientation,
            value_min,
            value_max,
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

        self.value_min = value_min
        self.value_max = value_max
        # variable to store last read normalized (0..1 float per sensor) state
        self.float_state = [0] * self.sensors_number

    def setup(self):
        # open SPI bus
        self.spi = spidev.SpiDev()
        self.spi.open(*self.SPI_DEVICE)
        self.spi.max_speed_hz = self.SPI_SPEED

        # update direction values
        self.update_dirs()

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

    def normalize(self, value):
        '''Converts SPI value to 0..1 calculated from max-min calibrated values

        Arguments:
            val {int} -- value read from SPI channel

        Returns:
            [float] -- value 0..1 calculated from max-min
            calibrated values and value read from SPI channel
        '''

        if value > self.value_max:
            value = self.value_max

        return (self.value_max - value) / (self.value_max - self.value_min)

    def input_binary(self, value):
        return int(value > self.value_min)

    def get_state(self):
        ret = 0

        for i in range(0, self.sensors_number):
            # get value from SPI channel
            data = self.spi_read(self.sensors[i])
            self.float_state[i] = self.normalize(data)

            # convert it to binary output
            inp = self.input_binary(data)

            if self.invert:
                ret += abs(inp - 1) << (self.sensors_number - i - 1)
            else:
                ret += inp << (self.sensors_number - i - 1)

        self.stack.put(ret)
        return ret

    def is_straight(self, state):
        return state & self.STRAIGHT > 0

    def is_turned(self, state):
        return (
            state & self.LEFT > 0 or
            state & self.RIGHT)

    def get_value(self, state):
        a, b = 0, 0
        for i in range(0, self.sensors_number):
            c = self.float_state[i]
            print(c)
            a += 1000 * c * i
            b += c

        if b == 0:
            b = 1

        return a / b
