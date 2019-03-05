class ChassisBase(object):

    def __init__(self):
        self.__on_move = []
        self.__on_rotate = []
        self.__moving = False
        self.do_turn_brake = True

    def rotate(self, degrees, stop_function=None):
        self.__trigger_on_rotate()

    def move(self):
        self.__moving = True
        self.__trigger_on_move()

    def stop(self, breaks=True):
        self.__moving = False
        pass

    def is_moving(self):
        return self.__moving

    def add_on_move_callback(self, on_move):
        self.__on_move.append(on_move)

    def add_on_rotate_callback(self, on_rotate):
        self.__on_rotate.append(on_rotate)

    def __trigger_on_move(self):
        """
        Triggers on_move events with current orientation
        :return: None
        """
        for on_move in self.__on_move:
            on_move(self)

    def __trigger_on_rotate(self):
        """
        Triggers on_rotate events with current orientation
        :return: None
        """
        for on_rotate in self.__on_rotate:
            on_rotate(self)
