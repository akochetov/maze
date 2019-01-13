from misc.pid import PID


class RPiLineSensorPID(object):
    def __init__(self, pid_settings, sensor, state_action, ok_state_value):
        self.pid = pid = PID(*pid_settings)
        self.sensor = sensor
        self.state_action = state_action
        self.ok_state_value = ok_state_value

    def get_pid(self):
        sensors_data = self.sensor.get_sensors_data()

        todo = state_action.get_action(sensors_data)

        if todo is None:
            actual = state_action.get_state(sensors_data)

            ret = pid.get(self.ok_state_value, actual)

            print('{}\tSensors: {}\tActual: {} Error: {} PID: {}'.format(
                datetime.now(),
                sensors_data,
                actual,
                self.ok_state_value - actual,
                ret))
            return ret

        return None
