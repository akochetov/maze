from brains.brain_base import BrainBase
from brains.direction import Direction

from threading import Thread
from time import sleep

class ThinkThread(Thread):

    def __init__(self, car):
        super().__init__()
        
        self.car = car

    def start(self):
        self.awake = True
        return super().start()

    def run(self):
        for i in range(0,1000):
            if not self.awake:
                break

            sleep(0.003)

            if self.car.is_out():
                self.awake = False
                break

            
            self.left_hand_search(self.car)
            #self.right_hand_search(self.car)

    def exit(self):
        self.awake = False


    def left_hand_search(self, car):
        state = str(car.sensors[0].get_state())

        if state.find("[1, 1, ")>=0:
            car.stop()
            car.move(Direction.LEFT)
            car.move(Direction.FORWARD)
        else:
            if state[7] == "1":
                car.move(Direction.FORWARD)
            else:
                car.stop()
                car.move(Direction.RIGHT)
                car.move(Direction.FORWARD)

    def right_hand_search(self, car):
        state = str(car.sensors[0].get_state())

        if state.find(", 1, 1]")>=0:
            car.stop()
            car.move(Direction.RIGHT)
            car.move(Direction.FORWARD)
        else:
            if state[7] == "1":
                car.move(Direction.FORWARD)
            else:
                car.stop()
                car.move(Direction.LEFT)
                car.move(Direction.FORWARD)


class HandSearchBrain(BrainBase):
    def think(self, car):
        self.thread = ThinkThread(car)
        self.thread.start()

    def is_still_thinking(self):
        return self.thread.awake
