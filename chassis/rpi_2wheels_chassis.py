from chassis.chassis_base import ChassisBase
from chassis.pwm_motor import PWMMotor
from time import sleep
from threading import Thread


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

        print('Power {} {}'.format(l, r))

        chassis.lmotor.rotate(True, l)
        chassis.rmotor.rotate(True, r)

        return True

    def run(self):
        while self.awake and self.do():
            sleep(self.chassis.frequency)

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

        self.lmotor = PWMMotor(*lmotor_settings.values(), pwm_frequency=pwm)
        self.rmotor = PWMMotor(*rmotor_settings.values(), pwm_frequency=pwm)
        self.lmotor.setup()
        self.rmotor.setup()

        self.left_motor_power = left_motor_power
        self.right_motor_power = right_motor_power
        self.turn_time = turn_time

        self.sensor_pid = sensor_pid
        self.frequency = frequency

        print('Initialized RPi chassis: {}'.format(self.__dict__))

        self.move_thread = RPi2WheelsMoveThread(self)

    def rotate(self, degrees):
        self.stop()

        if degrees == 180:
            self.lmotor.rotate(False, self.left_motor_power)
            self.rmotor.rotate(True, self.right_motor_power)
            sleep(self.turn_time * 2)
        else:
            self.lmotor.rotate(degrees == 90, self.left_motor_power)
            self.rmotor.rotate(degrees == -90, self.right_motor_power)
            sleep(self.turn_time)

        self.stop()

    def is_moving(self):
        return self.move_thread.awake

    def move(self):
        if self.is_moving():
            return True

        self.move_thread = RPi2WheelsMoveThread(self)
        self.move_thread.start()
        return True

    def stop(self):
        import traceback
        import sys
        print('Stopping motors...')
        traceback.print_stack(file=sys.stdout)

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

        print('GPIO PWMs de-initialized.')
