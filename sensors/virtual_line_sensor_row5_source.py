from line_sensor_source_base import LineSensorSourceBase


class VirtualLineSensorRow5(LineSensorSourceBase):
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

    def get_state(self):
        """
        Measures distance in steps to the wall in front of sensor
        :return: 0 if wall is close and no step can be made, or number of steps to the wall
        """
        ret = [0]*5
        pos = [self.maze.get_position()]*3

        if self.orientation == Orientation.WEST:                
            pos[0][0] += 1
            pos[1][1] -= 1
            pos[2][0] -= 1
        if self.orientation == Orientation.EAST:
            pos[0][0] -= 1
            pos[1][1] += 1
            pos[2][0] += 1
        if self.orientation == Orientation.NORTH:
            pos[0][1] -= 1
            pos[1][0] -= 1
            pos[2][1] += 1
        if self.orientation == Orientation.SOUTH:
            pos[0][1] -= 1
            pos[1][0] += 1
            pos[2][1] += 1

        for i in range(1,3):
            try:
                ret[i] = int(self.maze.test_if_wall(pos[0],pos[1]))
            except:
                pass

        ret[0] = ret[1]
        ret[4] = ret[3]

        return ret
