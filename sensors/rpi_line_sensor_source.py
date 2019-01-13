from sensors.line_sensor_source_base import LineSensorSourceBase
import RPi.GPIO as GPIO


class RPiLineSensorSource(LineSensorSourceBase):
    '''
    RPi implementation of digital line sensor with 5 IRs in line
    '''
    def __init__(self, sensors, orientation, invert=False):
        super().__init__(orientation)
        self.__sensors = sensors
        self.__invert = invert
        self._pins_number = len(self.__sensors)
        self.setup()

    def setup(self):
        for sensor in self.__sensors:
            # print('Calling GPIO.SETUP/GPIO.IN for pin {}'.format(sensor))
            GPIO.setup(sensor, GPIO.IN)

    def get_state(self):
        ret = [0]*self._pins_number
        for i in range(0, self._pins_number):
            ret[i] = GPIO.input(self.__sensors[i])

        return ret
