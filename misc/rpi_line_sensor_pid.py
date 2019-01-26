from misc.pid import PID
from misc.log import log


class RPiLineSensorPID(object):
    def __init__(self, pid_settings, sensor, ok_state_value):
        self.pid = PID(*pid_settings)
        self.sensor = sensor
        self.ok_state_value = ok_state_value

    def get_pid(self):
        actual = self.sensor.get_value()

        if actual is None:
            return None

        ret = self.pid.get_simple(self.ok_state_value, actual)

        log('Sensors: {}\tActual: {} Error: {} PID: {}'.format(
            bin(self.sensor.get_state()),
            actual,
            self.ok_state_value - actual,
            ret))

        return ret
