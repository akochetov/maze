from sensors.line_sensor_source_base import LineSensorSourceBase
from misc.orientation import Orientation
from misc.direction import Direction


class VirtualLineSensorSource(LineSensorSourceBase):
    """
    Car sensor. Measures distance to a wall in front of sensor
    """
    LEFT = 0b00011

    RIGHT = 0b11000

    FORWARD = 0b00100

    OFF = 0b00000

    def __init__(self, maze_world, orientation):
        """
        Constructor. Takes maze and initial sensor orientation
        :param maze_state: MazeState instance
        :param orientation: Orentation instance, pointing initial sensor
        orientation
        """
        super().__init__(orientation)
        self.maze = maze_world

    def get_state(self):
        """
        Measures distance in steps to the wall in front of sensor
        :return: 0 if wall is close and no step can be made, or number of
        steps to the wall
        """
        ret = 0
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
                ret += int(not self.maze.test_if_wall(
                    pos[i-1][0],
                    pos[i-1][1]
                    )) << i
            except:
                pass

        ret += (ret & 2) >> 1
        ret += (ret & 8) << 1

        return ret

    def get_directions(self):
        ret = []
        state = self.get_state()

        if self.__find_direction(state, self.LEFT):
            ret.append(Direction.LEFT)

        if self.__find_direction(state, self.RIGHT):
            ret.append(Direction.RIGHT)

        if self.__find_direction(state, self.FORWARD):
            ret.append(Direction.FORWARD)

        if self.__find_direction(state, self.OFF):
            ret.append(Direction.BACK)

        return ret

    def __find_direction(self, state, direction):
        return state & direction > 0 or state == direction
