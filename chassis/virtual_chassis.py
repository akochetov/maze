from chassis.chassis_base import ChassisBase
from worlds.virtual_world import VirtualWorld
from threading import Thread
from time import sleep

class VirtualMoveThread(Thread):

    def __init__(self, world, move_duration_sec):
        super().__init__()
        
        self.awake = False
        self.world = world
        self.move_duration_sec = move_duration_sec

    def start(self):
        self.awake = True
        return super().start()

    def run(self):
        while self.world.move() and self.awake:
            sleep(self.move_duration_sec)
        self.awake = False

    def exit(self):
        self.awake = False


class VirtualChassis(object):
 
    def __init__(self, world, move_duration_sec):
        super().__init__()

        self.world = world
        self.move_duration_sec = move_duration_sec
        self.move_thread = VirtualMoveThread(self.world, self.move_duration_sec)

    def rotate(self, degrees):
        pass

    def move(self):
        self.stop()
        self.move_thread = VirtualMoveThread(self.world, self.move_duration_sec)
        self.move_thread.start()
        return True

    def stop(self):
        self.move_thread.exit()

    def is_moving(self):
        return self.move_thread.awake
