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

    def rotate(self, cw):
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
        self.chassis.rotate(90 if cw else -90)

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

    def stop(self):
        self.chassis.stop()

    def move(self, direction):
        """
        Move car one step in Direction.
        In case it is FORWARD, moves where current Orientation is heading.
        If LEFT or RIGHT, turns first (changes Orientation) and quits.
        :param direction: Direction where to move
        """
        if direction == Direction.LEFT:
            self.rotate_ccw()
            return
        if direction == Direction.RIGHT:
            self.rotate_cw()
            return
        if direction == Direction.BACK:
            self.rotate_cw()
            self.rotate_cw()
            return

        self.chassis.move()

    def is_moving(self):
        self.chassis.is_moving()

    def is_out(self):
        """
        Checks whether car is now out of maze (exit found)
        :return: True if exit is found, False otherwise
        """
        return self.world.is_out(self.sensors)
