from worlds.world_base import WorldBase
from brains.orientation import Orientation

class MazePoint:
    """
    "Enum" for maze objects and their transcoding from string (chars) to objects such as wall, empty space, source and goal
    """
    def __init__(self):
        """
        Dummy init to avoid warnings
        """
        pass

    SOURCE = 'S'
    GOAL = 'G'
    WALL = 'X'
    SPACE = ' '
    POS = '*'


class VirtualWorld(WorldBase):
    """
    Maze. Loads it's state and interacts with obcejts in maze, such as cars and sensors
    """
    def __init__(self,file=None):
        """
        Constructor setting up initial position, goal point and optionally loads maze from text file
        :param file: file to load maze from or None if no load is needed
        """
        self.position = [0, 0]
        self.goal = [0, 0]
        self.state = []
        self.orientation = Orientation.SOUTH

        if file is None:
            return

        f = open(file)
        try:
            self.load(f)
        except:
            pass
        f.close()

    def set_orientation(self, orientation):
        self.orientation = orientation

    def refresh_points(self):
        """
        Loads start (source) and goal points
        """
        self.position = [0, 0]
        for i in range(0, len(self.state)):
            line = self.state[i]
            for j in range(0, len(line)):
                if line[j] == MazePoint.SOURCE:
                    self.set_position(i, j)
                if line[j] == MazePoint.GOAL:
                    self.set_goal(i, j)

    def get_position(self):
        """
        Returns current object position on a maze.
        For now only one car is supported
        :return: List of 2 values, x (row) and y (column)
        """
        return [self.position[0],self.position[1]]

    def set_position(self, x, y):
        """
        Changes car position in maze. Unmarks previous position (puts space) and marks new one with *
        :param x: row where to put a car
        :param y: column where to put a car
        :return:
        """
        if self.state[self.position[0]][self.position[1]] == MazePoint.POS:
            self.state[self.position[0]][self.position[1]] = MazePoint.SPACE
        self.position = [x, y]
        self.state[self.position[0]][self.position[1]] = MazePoint.POS

    def set_goal(self, x, y):
        """
        Sets maze goal point. When it is reached, this means exit is found
        :param x: row where to put exit
        :param y: column where to put exit
        """
        self.goal = [x, y]

    def load(self, input):
        """
        Load maze from source (can be file or any Stream)
        :param input: input stream
        """
        for line in input:
            l = []
            self.state.append(l)
            for char in line:
                if char != '\n':
                    l.append(char)
        self.refresh_points()

    def save(self, output):
        """
        Saves maze in a stream as text
        :param output: output stream
        """
        for line in self.state:
            for char in line:
                output.write(char)
            output.write('\n')
    

    def move(self):
        return self._move(self.orientation == Orientation.WEST,
                       self.orientation == Orientation.EAST,
                       self.orientation == Orientation.SOUTH,
                       self.orientation == Orientation.NORTH)

    def _move(self, west, east, south, north):
        """
        Tries to move an object (Car) in a maze. If destination is a wall - no move will happen
        :param west: True or False. Whether to move west.
        :param east: True or False. Whether to move east.
        :param south: True or False. Whether to move south.
        :param north: True or False. Whether to move north.
        """
        moves = 0
        if west and self.position[0] > 0 and self.state[self.position[0]][self.position[1] - 1] != MazePoint.WALL:
            moves += 1
            self.set_position(self.position[0], self.position[1] - 1)

        if east and self.position[0] < len(self.state[0])-1 and self.state[self.position[0]][self.position[1] + 1] != MazePoint.WALL:
            moves += 1
            self.set_position(self.position[0], self.position[1] + 1)

        if north and self.position[1] > 0 and self.state[self.position[0] - 1][self.position[1]] != MazePoint.WALL:
            moves += 1
            self.set_position(self.position[0] - 1, self.position[1])

        if south and self.position[1] < len(self.state)-1 and self.state[self.position[0] + 1][self.position[1]] != MazePoint.WALL:
            moves += 1
            self.set_position(self.position[0] + 1, self.position[1])

        # return True if all moves were accomplished
        return moves == [west,east,north,south].count(True)

    def test_if_wall(self, x, y):
        """
        Checks if given position is a wall or not
        :param x: row to test
        :param y: column to test
        :return: True if a wall, False is space, source or goal
        """
        return self.state[x][y] == MazePoint.WALL

    def is_out(self, sensors):
        """
        Checks whether current position is now out of maze (exit found)
        :return: True if exit is found, False otherwise
        """
        return self.position == self.goal
