from misc.pid import PID
from misc.log import log


class RPiLineSensorPID(object):
    def __init__(self, pid_settings, sensor, state_action, ok_state_value):
        self.pid = PID(*pid_settings)
        self.sensor = sensor
        self.state_action = state_action
        self.ok_state_value = ok_state_value

    def get_pid(self):
        sensors_data = self.sensor.get_state()

        actual = self.state_action.get_state(sensors_data)

        ret = self.pid.get(self.ok_state_value, actual)

        log('Sensors: {}\tActual: {} Error: {} PID: {}'.format(
            sensors_data,
            actual,
            self.ok_state_value - actual,
            ret))

        return ret
