class Orientation:
    """
    Orientation of maze, car etc. Means west, east, south and north.
    To be replaced with angle against north in the future
    """
    def __init__(self):
        """
        Dummy init to eliminate warnings
        """
        pass

    WEST = 'WEST'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    NORTH = 'NORTH'

    # list used to change orientation by changing list index -1 for counter
    # clock wise and +1 for clock wise rotations
    rotation = [NORTH, EAST, SOUTH, WEST]

    @staticmethod
    def rotate(initial_orientation, cw):
        """
        Static method. Changes orientation
        :param initial_orientation: Orientation which has to be changed
        :param cw: ClockWise. True or False. In case of False rotates counter
        clock wise
        :return: new orientation after rotation of initial_orientation
        """
        index = Orientation.rotation.index(initial_orientation)
        index = index + 1 if cw else index - 1
        if index >= len(Orientation.rotation):
            index = 0
        if index < 0:
            index = len(Orientation.rotation) - 1
        return Orientation.rotation[index]

    @staticmethod
    def rotate_cw(initial_orientation):
        """
        Rotate clock wise
        """
        return Orientation.rotate(initial_orientation, True)

    @staticmethod
    def rotate_ccw(initial_orientation):
        """
        Rotate counter clock wise
        """
        return Orientation.rotate(initial_orientation, False)

    @staticmethod
    def flip(initial_orientation):
        """
        Rotate 180 degrees
        """
        return Orientation.rotate(
            Orientation.rotate(initial_orientation, False),
            False
            )
