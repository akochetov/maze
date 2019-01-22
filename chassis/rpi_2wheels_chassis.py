from chassis.chassis_base import ChassisBase
from chassis.pwm_motor import PWMMotor
from misc.log import log
from time import sleep
from time import time
from threading import Thread

# how frequently check sensors state when turning
TURN_FREQ = 1 / 100


class RPi2WheelsMoveThread(Thread):
    def __init__(self, chassis):
        super().__init__()

        self.awake = False
        self.chassis = chassis

    def start(self):
        self.awake = True
        return super().start()

    def do(self):
        chassis = self.chassis
        power = (chassis.left_motor_power + chassis.right_motor_power) / 2

        pow = chassis.sensor_pid.get_pid()

        if pow is None:
            return False

        pow = pow if (abs(pow) <= power) else power * pow / abs(pow)

        [l, r] = [chassis.left_motor_power, chassis.right_motor_power]

        if pow > 0:
            l -= int(pow)
            r += int(pow)
        if pow < 0:
            l -= int(pow)
            r += int(pow)

        # log('Power {} {}'.format(l, r))

        chassis.lmotor.rotate(True, l)
        chassis.rmotor.rotate(True, r)

        return True

    def run(self):
        while self.awake and self.do():
            sleep(self.chassis.sleep_time)

        self.awake = False

    def exit(self):
        self.awake = False


class RPi2WheelsChassis(ChassisBase):
    def __init__(
            self,
            lmotor_settings,
            rmotor_settings,
            left_motor_power,
            right_motor_power,
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

        self.left_motor_power = left_motor_power
        self.right_motor_power = right_motor_power
        self.turn_time = turn_time

        self.sensor_pid = sensor_pid
        self.sleep_time = 1.0 / frequency

        log('Initialized RPi chassis: {}'.format(self.__dict__))

        self.move_thread = RPi2WheelsMoveThread(self)

    def rotate(self, degrees, stop_function=None):
        self.stop()

        log('Stopped. Turning...')

        if degrees == 180:
            self.lmotor.rotate(False, self.left_motor_power)
            self.rmotor.rotate(True, self.right_motor_power)
        else:
            self.lmotor.rotate(degrees == 90, self.left_motor_power)
            self.rmotor.rotate(degrees == -90, self.right_motor_power)

        if stop_function is None:
            sleep(self.turn_time * float(abs(degrees)) / 90.0)
        else:
            start = time()
            # first have a sleep equal to half turn to get car started to turn
            sleep(self.turn_time * float(abs(degrees)) / 180.0)

            enough_time = 4 * self.turn_time * float(abs(degrees)) / 90.0
            while not stop_function() and time() - start < enough_time:
                sleep(TURN_FREQ)

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
        if self.is_moving():
            self.move_thread.exit()
            self.move_thread.join()

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
