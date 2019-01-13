from worlds.world_base import WorldBase
from time import time


class LineWorld(WorldBase):

    IS_OUT = '[1, 1, 1, 1, 1]'
    CONFIDENCE_TIMEOUT_SEC = 0.5

    def __init__(self):
        super().__init__()

        self.reset()

    def reset(self):
        self.sensor_data = 0
        self.last_sensing = 0

    def is_out(self, sensors_data):
        for i in range(len(LineWorld.IS_OUT)):
            if sensors_data[i] != IS_OUT[1]:
                self.sensor_data = 0
                return False

        if self.sensor_data > 0 and time()-self.last_sensing < LineWorld.CONFIDENCE_TIMEOUT_SEC:
            self.reset()
            return True

        self.sensor_data += 1
        self.last_sensing = time()
        return False
