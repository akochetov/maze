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

    def __init__(
            self,
            lmotor_settings,
            rmotor_settings,
            left_motor_pow,
            right_motor_pow,
            turn_time,
            brake_time,
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
        self.brake_time = brake_time

        self.sensor_pid = sensor_pid
        self.sleep_time = 1.0 / frequency

        self.move_thread = RPi2WheelsMoveThread(self)

    def _pid_to_power(self, pid, is_turning):
        # go fast by default
        # if we are at crossing - slow down!
        speed = self.SLOW if (is_turning and self.do_turn_brake) else self.FAST

        l, r = (
            self.left_motor_pow[speed],
            self.right_motor_pow[speed]
        )

        if pid >= 0:
            if pid > r:
                pid = r
            return l, int(r - pid)

        if pid < 0:
            if -pid > l:
                pid = -l
            return int(l + pid), r

    def _move(self):
        # get PID value based on sensor values
        # this is to get robot rolling straight
        pid, is_turning = self.sensor_pid.get_pid()

        l, r = self._pid_to_power(pid, is_turning)

        log('Power {} {}'.format(l, r))

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

            enough_time = 3 * self.turn_time * float(abs(degrees)) / 90.0
            while not stop_function() and time() - start < enough_time:
                pass

        # breaking...
        if degrees == 180:
            self.lmotor.rotate(True, self.left_motor_pow[self.TURN])
            self.rmotor.rotate(False, self.right_motor_pow[self.TURN])
            sleep(self.brake_time / 2)
        else:
            self.lmotor.rotate(degrees == -90, self.left_motor_pow[self.TURN])
            self.rmotor.rotate(degrees == 90, self.right_motor_pow[self.TURN])
            sleep(self.brake_time / 2)

        # move slightly fwd after turning to get sensor to the line
        # self.lmotor.rotate() # True, self.left_motor_pow[self.TURN])
        # self.rmotor.rotate() # True, self.right_motor_pow[self.TURN])
        # sleep(self.brake_time)

        self.stop()
        super().rotate(degrees, stop_function)
        log('Turning finished.')

    def is_moving(self):
        return self.move_thread.awake

    def move(self):
        if self.is_moving():
            return True

        self.move_thread = RPi2WheelsMoveThread(self)
        self.move_thread.start()
        return True

    def stop(self, breaks=True):
        moving = self.is_moving()

        if moving:
            self.move_thread.exit()
            if self.move_thread.is_alive():
                self.move_thread.join()

        if breaks and moving:
            log('Breaking...')
            # active break
            self.lmotor.rotate(False)
            self.rmotor.rotate(False)
            sleep(self.brake_time)
            self.lmotor.stop()
            self.lmotor.stop()
            log('Breakin done.')

        # if moving:
        #    self.move_thread.join()

        if self.lmotor is not None:
            self.lmotor.stop()

        if self.rmotor is not None:
            self.rmotor.stop()

        # reset pid error
        self.sensor_pid.reset()

    def __del__(self):
        if self.lmotor is not None:
            self.lmotor.stop()
            self.lmotor.cleanup()

        if self.rmotor is not None:
            self.rmotor.stop()
            self.rmotor.cleanup()

        log('GPIO PWMs de-initialized.')
