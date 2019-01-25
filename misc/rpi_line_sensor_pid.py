from misc.pid import PID
from misc.log import log


class RPiLineSensorPID(object):
    def __init__(self, pid_settings, sensor, ok_state_value):
        self.pid = PID(*pid_settings)
        self.sensor = sensor
        self.ok_state_value = ok_state_value

    def get_pid(self):
        sensors_data = self.sensor.get_state()

        if sensors_data == 0 or sensors_data == 0b10000:
            return None

        actual = (
            sensors_data & 0b00001 * 0 +
            sensors_data & 0b00010 * 1000 +
            sensors_data & 0b00100 * 2000 +
            sensors_data & 0b01000 * 3000 +
            sensors_data & 0b10000 * 4000
            ) / (
            sensors_data & 0b00001 +
            sensors_data & 0b00010 +
            sensors_data & 0b00100 +
            sensors_data & 0b01000 +
            sensors_data & 0b10000
            )

        ret = self.pid.get_simple(self.ok_state_value, actual)

        log('Sensors: {}\tActual: {} Error: {} PID: {}'.format(
            sensors_data,
            actual,
            self.ok_state_value - actual,
            ret))

        return ret
