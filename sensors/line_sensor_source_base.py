class LineSensorSourceBase(object):
    '''
    RPi abstract class for line sensors
    '''
    def __init__(self, orientation):
        self.orientation = orientation

    def bits_to_str(self, data):
        ret = ''
        for d in data:
            ret += str(d)
        return ret

    def get_state(self):
        pass

    def get_directions(self):
        pass

    def reset(self):
        pass
