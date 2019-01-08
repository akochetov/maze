from sensors.distance_sensor import Sensor
from brains.orientation import Orientation
from brains.direction import Direction
from chassis.chassis_base import ChassisBase
from worlds.world_base import WorldBase

class Car(object):
    """
    Car. Has sensors and has a maze reference.
    Interacts with maze through sensors and moves within maze.
    """
    def __init__(self, world, chassis, sensors, orientation):
        """
        Constructor. Set instance vars: maze and orientation. Create and setup sensors
        :param maze_state: MazeState instance
        :param orientation: Orientation instance - where car is heading initially
        """
        self.on_move = []
        self.on_rotate = []
        self.on_crossing = []

        self.world = world
        self.chassis = chassis
        self.orientation = orientation

        self.sensors = sensors

    def get_crossing_data(self):
        return 0

    def rotate(self, cw):
        """
        Car turning.
        :param cw: ClockWise. True or False. In case of False rotates counter clock wise
        """

        # rotate car
        self.chassis.rotate(90 if cw else -90)
        self.orientation = Orientation.rotate(self.orientation, cw)
        self.world.set_orientation(self.orientation)

        # "rotate" sensors too
        for sensor in self.sensors:
            sensor.source.orientation = Orientation.rotate(sensor.source.orientation, cw)

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

        #sensors = self.get_crossing_data()
        self.chassis.move()
        self.trigger_on_move()

        # detect if we reached crossing and if so - fire events
        #if sensors != self.get_crossing_data() and self.get_crossing_data() != Car.SENSOR_FWD:
        #    self.trigger_on_crossing()

    def is_moving(self):
        self.chassis.is_moving()

    def is_out(self):
        """
        Checks whether car is now out of maze (exit found)
        :return: True if exit is found, False otherwise
        """
        return self.world.is_out(self.sensors)


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
