from chassis.pwm_motor import PWMMotor
from time import sleep

lmotor = PWMMotor(13, 5, 6, pwm_frequency=40)
rmotor = PWMMotor(19, 20, 21, pwm_frequency=40)
lmotor.rotate(power=33)
rmotor.rotate(power=33)
sleep(5)
lmotor.rotate(False)
rmotor.rotate(False)
sleep(5)
lmotor.rotate(True)
rmotor.rotate(False)
sleep(5)
lmotor.rotate(False)
rmotor.rotate(True)
sleep(5)
lmotor.cleanup()
rmotor.cleanup()
