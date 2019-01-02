from sensor import Sensor
from orientation import Orientation
from direction import Direction


class Car(object):

    SENSOR_LEFT = 1
    SENSOR_FWD = 2
    SENSOR_RIGHT = 4

    """
    Car. Has sensors and has a maze reference.
    Interacts with maze through sensors and moves within maze.
    """
    def __init__(self, maze_state, orientation):
        """
        Constructor. Set instance vars: maze and orientation. Create and setup sensors
        :param maze_state: MazeState instance
        :param orientation: Orientation instance - where car is heading initially
        """
        self.on_move = []
        self.on_rotate = []
        self.on_crossing = []

        self.maze = maze_state
        self.orientation = orientation

        self.sensors = [
            Sensor(maze_state,Orientation.rotate_ccw(orientation)),
            Sensor(maze_state,orientation),
            Sensor(maze_state,Orientation.rotate_cw(orientation))
        ]

    def get_crossing_data(self):
        return  (Car.SENSOR_LEFT if self.sensors[0].get_distance() else 0) +\
                (Car.SENSOR_FWD if self.sensors[1].get_distance() else 0) +\
                (Car.SENSOR_RIGHT if self.sensors[2].get_distance() else 0)

    def rotate(self, cw):
        """
        Car turning.
        :param cw: ClockWise. True or False. In case of False rotates counter clock wise
        """

        # rotate car
        self.orientation = Orientation.rotate(self.orientation, cw)

        # "rotate" sensors too
        for sensor in self.sensors:
            sensor.orientation = Orientation.rotate(sensor.orientation, cw)

        self.trigger_on_rotate()

    def rotate_cw(self):
        """
        Rotate car clock wise
        """
        self.rotate(True)

    def rotate_ccw(self):
        """
        Rotate car counter clock wise
        """
        self.rotate(False)

    def move(self, direction):
        """
        Move car one step in Direction.
        In case it is FORWARD, moves where current Orientation is heading.
        If LEFT or RIGHT, turns first (changes Orientation) and then makes one step forward.
        :param direction: Direction where to move
        """
        if direction == Direction.LEFT:
            self.rotate_ccw()
        if direction == Direction.RIGHT:
            self.rotate_cw()

        sensors = self.get_crossing_data()
        if (self.maze.move(self.orientation == Orientation.WEST,
                       self.orientation == Orientation.EAST,
                       self.orientation == Orientation.SOUTH,
                       self.orientation == Orientation.NORTH)):
            self.trigger_on_move()

            # detect if we reached crossing and if so - fire events
            if direction == Direction.FORWARD and sensors != self.get_crossing_data() and self.get_crossing_data() != Car.SENSOR_FWD:
                self.trigger_on_crossing()

    def is_out(self):
        """
        Checks whether car is now out of maze (exit found)
        :return: True if exit is found, False otherwise
        """
        return self.maze.is_out()


    def trigger_on_move(self):
        """
        Triggers on_move events with current orientation
        :return: None
        """
        for on_move in self.on_move:
            on_move(self, self.orientation)

    def trigger_on_rotate(self):
        """
        Triggers on_rotate events with current orientation
        :return: None
        """
        for on_rotate in self.on_rotate:
            on_rotate(self, self.orientation)

    def trigger_on_crossing(self):
        """
        Triggers on_crossing events with current orientation
        :return: None
        """
        for on_crossing in self.on_crossing:
            on_crossing(self, self.orientation)
