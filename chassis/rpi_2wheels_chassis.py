from chassis.chassis_base import ChassisBase
from chassis.pwm_motor import PWMMotor


class RPi2WheelsChassis(ChassisBase):

    def __init__(self, lmotor_settings, rmotor_settings, pwm):
        self.lmotor = PWMMotor(*lmotor_settings, pwm_frequency=pwm)
        self.rmotor = PWMMotor(*rmotor_settings, pwm_frequency=pwm)
        self.lmotor.setup()
        self.rmotor.setup()

    def rotate(self, degrees):
        pass

    def move(self):
        lmotor.rotate(True, l)
        rmotor.rotate(True, r)

    def stop(self):
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