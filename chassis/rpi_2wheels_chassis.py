from chassis.chassis_base import ChassisBase
from chassis.pwm_motor import PWMMotor

class RPi2WheelsChassis(ChassisBase):

	def __init__(self, lmotor, rmotor):
		self.lmotor = PWMMotor(*settings.LEFT_MOTOR.values(),pwm_frequency=settings.PWM)
		self.rmotor = PWMMotor(*settings.RIGHT_MOTOR.values(),pwm_frequency=settings.PWM)
		self.lmotor.setup()
		self.rmotor.setup()


	def rotate(self, degrees):
		pass


	def move(self):
		pass


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