from worlds.world_base import WorldBase
from time import time


class LineWorld(WorldBase):
    def __init__(self, state_out, reps_when_out):
        self.state_out = state_out
        self.reps_when_out = reps_when_out
        self.reps = 0

    def is_out(self, sensors_data):
        if str(sensors_data) != self.state_out:
            self.reps = 0
            return False
        self.res += 1
        return self.reps >= self.reps_when_out
