from line_sensor_source_base import LineSensorSourceBase
import RPi.GPIO as GPIO


class RPiLineSensorSource(LineSensorSourceBase):
    '''
    RPi implementation of digital line sensor with 5 IRs in line
    '''
    def __init__(self, sensors, invert=False):
        self.__sensors = sensors
        self.__invert = invert
        self.setup()

    def setup(self):
        for sensor in self.__sensors:
            GPIO.setup(sensor, GPIO.IN)

    def get_sensors_data(self):
        str_to_ret = ''
        for sensor in self.__sensors:
            signal = GPIO.input(sensor)
            str_to_ret += str(int(not signal if self.__invert else signal))
        return str_to_ret
