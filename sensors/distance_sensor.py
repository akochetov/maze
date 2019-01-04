from brains.orientation import Orientation

class Sensor(object):
    """
    Car sensor. Measures distance to a wall in front of sensor
    """
    def __init__(self, maze_state, orientation):
        """
        Constructor. Takes maze and initial sensor orientation
        :param maze_state: MazeState instance
        :param orientation: Orentation instance, pointing initial sensor orientation
        """
        self.maze = maze_state
        self.orientation = orientation

    def get_distance(self):
        """
        Measures distance in steps to the wall in front of sensor
        :return: 0 if wall is close and no step can be made, or number of steps to the wall
        """
        ret = 0
        pos = self.maze.get_position()
        while True:
            if self.orientation == Orientation.WEST:
                pos[1] -= 1
            if self.orientation == Orientation.EAST:
                pos[1] += 1
            if self.orientation == Orientation.NORTH:
                pos[0] -= 1
            if self.orientation == Orientation.SOUTH:
                pos[0] += 1

            try:
                if self.maze.test_if_wall(pos[0],pos[1]):
                    break
            except:
                break

            ret += 1

        return ret
