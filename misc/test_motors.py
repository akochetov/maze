import RPi.GPIO as GPIO
from time import sleep
from datetime import  datetime
from pwm_motor import PWMMotor

#initializing motors
try:
	lmotor = {"EN":13,"IN1":5,"IN2":6}
	rmotor = {"EN":19,"IN1":20,"IN2":16}

	led = 15	#signal led pin (to indicate program status)

	power = 80	# in % from max 100%

	lmotor = PWMMotor(*lmotor.values())
	rmotor = PWMMotor(*rmotor.values())
	lmotor.setup()
	rmotor.setup()

	#setup led to indicate program status
	GPIO.setup(led,GPIO.OUT)
	GPIO.output(led,GPIO.HIGH)

	print('Rotating left motor...')
	lmotor.rotate(True, power)
	sleep(2)
	lmotor.stop()
	print('Left motor stopped.')

	print('Rotating right motor...')
	rmotor.rotate(True, power)
	sleep(2)
	rmotor.stop()
	print('Right motor stopped.')

	print('Going forward (both motors)...')
	lmotor.rotate(True, power)
	rmotor.rotate(True, power)
	sleep(4)
	lmotor.stop()
	rmotor.stop()
	print('Motors stopped.')
except KeyboardInterrupt:
    pass

lmotor.cleanup()
rmotor.cleanup()

GPIO.output(led,GPIO.LOW)
GPIO.cleanup()
