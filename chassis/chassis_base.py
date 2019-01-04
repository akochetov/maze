class ChassisBase(object):

    def __init__(self):
        self._moving = False
    
    def rotate(self, degrees):
        pass

    def move(self, throttle):
        self._moving = True
        pass

    def stop(self):
        self._moving = False
        pass

    def is_moving(self):
        return self._moving