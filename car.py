from sensors.distance_sensor import Sensor
from misc.orientation import Orientation
from misc.direction import Direction
from chassis.chassis_base import ChassisBase


class Car(object):
    """
    Car. Has sensors and has a maze reference.
    Interacts with maze through sensors and moves within maze.
    """
    def __init__(self, world, chassis, sensors, orientation):
        """
        Constructor. Set instance vars: maze and orientation.
        Create and setup sensors

        :param maze_state: MazeState instance
        :param orientation: Orientation instance - where car is heading
        initially
        """
        self.world = world
        self.chassis = chassis
        self.orientation = orientation

        self.sensors = sensors

    def turn_around(self, stop_function=None):
        """
        Car turning.
        :param cw: ClockWise. True or False. In case of False rotates counter
        clockwise
        """

        # rotate car
        self.orientation = Orientation.flip(self.orientation)
        self.world.set_orientation(self.orientation)

        # "rotate" sensors too
        for sensor in self.sensors:
            sensor.source.orientation = Orientation.flip(
                sensor.source.orientation
                )
            sensor.reset()
        self.chassis.rotate(180, stop_function=stop_function)

    def rotate(self, cw, stop_function=None):
        """
        Car turning.
        :param cw: ClockWise. True or False. In case of False rotates counter
        clockwise
        """

        # rotate car
        self.orientation = Orientation.rotate(self.orientation, cw)
        self.world.set_orientation(self.orientation)

        # "rotate" sensors too
        for sensor in self.sensors:
            sensor.source.orientation = Orientation.rotate(
                sensor.source.orientation, cw
                )
            sensor.reset()
        self.chassis.rotate(90 if cw else -90, stop_function=stop_function)

    def rotate_cw(self, stop_function=None):
        """
        Rotate car clock wise
        """
        self.rotate(True, stop_function=stop_function)

    def rotate_ccw(self, stop_function=None):
        """
        Rotate car counter clock wise
        """
        self.rotate(False, stop_function=stop_function)

    def stop(self):
        self.chassis.stop()

    def move(self, direction):
        """
        Move car one step in Direction.
        In case it is FORWARD, moves where current Orientation is heading.
        If LEFT or RIGHT, turns first (changes Orientation) and quits.
        :param direction: Direction where to move
        """
        if self.is_moving():
            return

        self.chassis.move()
        # doubtfull solution, but lets try:
        # this is required for virtual moves mainly
        # when car made first move, sensors have to be updated
        # to catch new data
        for sensor in self.sensors:
            sensor.reset()

    def is_moving(self):
        self.chassis.is_moving()

    def is_out(self):
        """
        Checks whether car is now out of maze (exit found)
        :return: True if exit is found, False otherwise
        """
        return self.world.is_out(self.sensors)
