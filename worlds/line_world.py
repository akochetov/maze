from worlds.world_base import WorldBase
from time import time


class LineWorld(WorldBase):
    def is_out(self, sensors):
        return sensors[0].get_directions() is None
