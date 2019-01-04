class LineSensorSourceBase(object):
    '''
    RPi abstract class for line sensors
    '''
    def __init__(self):
        self.callbacks = []

    def get_state(self):
        pass

    def trigger_state_change(self):
        for callback in self.callbacks:
            callback(self.state)

    def add_state_change_callback(self, callback):
        if self.callbacks.find(callback) < 0:
            self.callbacks.append(callback)

    def remove_state_change_callback(self, callback):
        if self.callbacks.find(callback) >= 0:
            self.callbacks.remove(callback)



