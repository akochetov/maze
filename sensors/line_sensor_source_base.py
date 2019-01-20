class LineSensorSourceBase(object):
    '''
    RPi abstract class for line sensors
    '''
    def __init__(self, orientation):
        self.orientation = orientation

    def get_state(self):
        pass

    def get_directions(self):
        pass
