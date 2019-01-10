from sensors.line_sensor_source_base import LineSensorSourceBase
from misc.orientation import Orientation


class VirtualLineSensorSource(LineSensorSourceBase):
    """
    Car sensor. Measures distance to a wall in front of sensor
    """
    def __init__(self, maze_world, orientation):
        """
        Constructor. Takes maze and initial sensor orientation
        :param maze_state: MazeState instance
        :param orientation: Orentation instance, pointing initial sensor
        orientation
        """
        self.maze = maze_world
        self.orientation = orientation

    def get_state(self):
        """
        Measures distance in steps to the wall in front of sensor
        :return: 0 if wall is close and no step can be made, or number of
        steps to the wall
        """
        ret = [0]*5
        pos = [
            self.maze.get_position(),
            self.maze.get_position(),
            self.maze.get_position()
            ]

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
            pos[0][1] += 1
            pos[1][0] += 1
            pos[2][1] -= 1

        # left and right most sensor - init with same data as two left and
        # right sensors from center
        for i in range(1, 4):
            try:
                ret[i] = int(not self.maze.test_if_wall(
                    pos[i-1][0],
                    pos[i-1][1]
                    ))
            except:
                pass

        ret[0] = ret[1]
        ret[4] = ret[3]

        return ret
