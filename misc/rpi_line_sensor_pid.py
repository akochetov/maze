from misc.pid import PID
from misc.log import log


class RPiLineSensorPID(object):
    def __init__(self, pid_settings, sensor, ok_state_value):
        self.pid = PID(*pid_settings)
        self.sensor = sensor
        self.ok_state_value = ok_state_value

    def get_weighted_actual(self, sensors_data):
        return (
            (sensors_data & 0b00001) * 0 +
            (sensors_data & 0b00010) / 2 * 1000 +
            (sensors_data & 0b00100) / 4 * 2000 +
            (sensors_data & 0b01000) / 8 * 3000 +
            (sensors_data & 0b10000) / 16 * 4000
            ) / (
            (sensors_data & 0b00001) +
            (sensors_data & 0b00010) / 2 +
            (sensors_data & 0b00100) / 4 +
            (sensors_data & 0b01000) / 8 +
            (sensors_data & 0b10000) / 16
            )

    def get_pid(self):
        sensors_data = self.sensor.get_state()

        if sensors_data == 0 or sensors_data == 0b10000:
            return None

        actual = self.get_weighted_actual(sensors_data)

        ret = self.pid.get_simple(self.ok_state_value, actual)

        log('Sensors: {}\tActual: {} Error: {} PID: {}'.format(
            bin(sensors_data),
            actual,
            self.ok_state_value - actual,
            ret))

        return ret
