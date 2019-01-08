class StateAction:
	def __init__(self, states, actions):
		self.states = states
		self.actions = actions


	def get_action(self, sensors_data):
		if sensors_data in self.actions:
			return self.actions[sensors_data]

		return None


	def get_state(self, sensors_data, default_state):
		if sensors_data in self.states:
			return self.states[sensors_data]

		return default_state

