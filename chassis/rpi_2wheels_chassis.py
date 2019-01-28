from chassis.chassis_base import ChassisBase
from chassis.pwm_motor import PWMMotor
from misc.log import log
from time import sleep
from time import time
from threading import Thread


class RPi2WheelsMoveThread(Thread):
    def __init__(self, chassis):
        super().__init__()

        self.awake = False
        self.chassis = chassis

    def start(self):
        self.awake = True
        return super().start()

    def run(self):
        while self.awake:
            self.chassis._move()
            sleep(self.chassis.sleep_time)

        self.awake = False

    def exit(self):
        self.awake = False


class RPi2WheelsChassis(ChassisBase):
    SLOW = "SLOW"
    FAST = "FAST"
    TURN = "TURN"

    BREAK_TIME = 1.0 / 8.0

    def __init__(
            self,
            lmotor_settings,
            rmotor_settings,
            left_motor_pow,
            right_motor_pow,
            turn_time,
            pwm,
            sensor_pid,
            frequency
            ):
        super().__init__()

        self.lmotor = PWMMotor(
            lmotor_settings["EN"],
            lmotor_settings["IN1"],
            lmotor_settings["IN2"],
            pwm_frequency=pwm)
        self.rmotor = PWMMotor(
            rmotor_settings["EN"],
            rmotor_settings["IN1"],
            rmotor_settings["IN2"],
            pwm_frequency=pwm)
        self.lmotor.setup()
        self.rmotor.setup()

        self.left_motor_pow = left_motor_pow
        self.right_motor_pow = right_motor_pow
        self.turn_time = turn_time

        self.sensor_pid = sensor_pid
        self.sleep_time = 1.0 / frequency

        log('Initialized RPi chassis: {}'.format(self.__dict__))

        self.move_thread = RPi2WheelsMoveThread(self)

    def _pid_to_power(self, pid):
        # go fast by default
        # if there is no PID detected (meaning that we are at crossing)
        # then slow down
        speed = self.SLOW if pid is None else self.FAST

        l, r = (
            self.left_motor_pow[speed],
            self.right_motor_pow[speed]
        )

        if pid is not None:
            l = l - int(abs(pid) - pid / 2)
            r = r - int(abs(pid) + pid / 2)

            if l < 0:
                l = 0
            if l > 100:
                l = 100
            if r < 0:
                r = 0
            if r > 100:
                r = 100

        return l, r

    def _move(self):
        # get PID value based on sensor values
        # this is to get robot rolling straight
        pid = self.sensor_pid.get_pid()

        l, r = self._pid_to_power(pid)

        # log('Power {} {}'.format(l, r))

        self.lmotor.rotate(True, l)
        self.rmotor.rotate(True, r)

    def rotate(self, degrees, stop_function=None):
        self.stop()

        log('Stopped. Turning...')

        if degrees == 180:
            self.lmotor.rotate(False, self.left_motor_pow[self.TURN])
            self.rmotor.rotate(True, self.right_motor_pow[self.TURN])
        else:
            self.lmotor.rotate(degrees == 90, self.left_motor_pow[self.TURN])
            self.rmotor.rotate(degrees == -90, self.right_motor_pow[self.TURN])

        if stop_function is None:
            sleep(self.turn_time * float(abs(degrees)) / 90.0)
        else:
            start = time()
            # first have a sleep equal to half turn to get car started to turn
            sleep(self.turn_time * float(abs(degrees)) / 180.0)

            enough_time = 4 * self.turn_time * float(abs(degrees)) / 90.0
            while not stop_function() and time() - start < enough_time:
                sleep(self.sleep_time / 2)

        if degrees == 180:
            self.lmotor.rotate(True)
            self.rmotor.rotate(False)
            sleep(self.BREAK_TIME)
        else:
            self.lmotor.rotate(degrees == -90)
            self.rmotor.rotate(degrees == 90)
            sleep(self.BREAK_TIME / 2)

        self.stop()

        log('Turning finished.')

    def is_moving(self):
        return self.move_thread.awake

    def move(self):
        if self.is_moving():
            return True

        self.move_thread = RPi2WheelsMoveThread(self)
        self.move_thread.start()
        return True

    def stop(self):
        moving = self.is_moving()

        if moving:
            self.move_thread.exit()
            self.move_thread.join()

            log('Breaking...')
            # active break
            self.lmotor.rotate(False)
            self.rmotor.rotate(False)
            sleep(self.BREAK_TIME)
            self.lmotor.stop()
            self.lmotor.stop()
            log('Breakin done.')

        # if moving:
        #    self.move_thread.join()

        if self.lmotor is not None:
            self.lmotor.stop()

        if self.rmotor is not None:
            self.rmotor.stop()

    def __del__(self):
        if self.lmotor is not None:
            self.lmotor.stop()
            self.lmotor.cleanup()

        if self.rmotor is not None:
            self.rmotor.stop()
            self.rmotor.cleanup()

        log('GPIO PWMs de-initialized.')
