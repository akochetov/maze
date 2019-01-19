from misc.log import log()


class StateAction:
    def __init__(self, states, actions):
        self.states = states
        self.actions = actions

    def get_action(self, sensors_data):
        data = str(sensors_data)
        if data in self.actions:
            log('Action detected. Signal: {}, action: {}'.format(
                data, self.actions[data]
                ))
            return self.actions[data]

        return None

    def get_state(self, sensors_data):
        data = str(sensors_data)
        if data in self.states:
            return self.states[data]

        return 0
