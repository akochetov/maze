from chassis.chassis_base import ChassisBase
from worlds.virtual_world import VirtualWorld
from threading import Thread
from time import sleep


class VirtualMoveThread(Thread):

    def __init__(self, chassis, world, move_duration_sec):
        super().__init__()

        self.awake = False
        self.world = world
        self.chassis = chassis
        self.move_duration_sec = move_duration_sec

    def start(self):
        self.awake = True
        return super().start()

    def do(self):
        if self.world.can_move():
            sleep(self.move_duration_sec)

            # make sure thread was not stopped during sleep
            if self.awake:
                self.world.move()

            return True

        return False

    def run(self):
        while self.awake and self.do():
            pass

        self.awake = False

    def exit(self):
        self.awake = False


class VirtualChassis(ChassisBase):

    def __init__(self, world, move_duration_sec):
        super().__init__()

        self.world = world
        self.move_duration_sec = move_duration_sec
        self.move_thread = VirtualMoveThread(
            self,
            self.world,
            self.move_duration_sec
            )

    def super_move(self):
        super().move()

    def rotate(self, degrees, stop_function=None):
        super().rotate(degrees)
        sleep(
            float(self.move_duration_sec) *
            float(abs(degrees)) /
            90.0)
        super().rotate(degrees)

    def move(self):
        if self.is_moving():
            return True

        self.move_thread = VirtualMoveThread(
            self,
            self.world,
            self.move_duration_sec
            )

        # first move has to be synchronously in virtual world
        # due to discrete moves
        self.move_thread.awake = True
        self.move_thread.do()

        self.move_thread.start()

        return True

    def stop(self, breaks=True):
        if self.move_thread.is_alive():
            self.move_thread.exit()
            self.move_thread.join()

    def is_moving(self):
        return self.move_thread.awake
