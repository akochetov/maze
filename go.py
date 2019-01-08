import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import misc.settings as settings
from chassis.pwm_motor import PWMMotor
from misc.pid import PID
from sensors.rpi_line_sensor_source import RPiLineSensorSource
from misc.state_action import StateAction

GPIO.setmode(GPIO.BCM)

sensor = RPiLineSensorSource(settings.LINE_SENSORS)

pid = PID(*settings.PID)
state_action = StateAction(settings.STATE_ERROR, settings.STATE_ACTION)

state_action_reps = 0
last_state_action = None

lmotor = None
rmotor = None

try:
	lmotor = PWMMotor(*settings.LEFT_MOTOR.values(),pwm_frequency=settings.PWM)
	rmotor = PWMMotor(*settings.RIGHT_MOTOR.values(),pwm_frequency=settings.PWM)
	lmotor.setup()
	rmotor.setup()

	while True:
		sensors_data = sensor.get_sensors_data()

		todo = state_action.get_action(sensors_data)

		if todo is None:
			# regular line following
			state_action_reps = 0

			actual = state_action.get_state(sensors_data, settings.STATE_OK)

			if sensors_data != '00000' and sensors_data != '11111':
				pow = pid.get(settings.STATE_OK, actual)
				pow = pow if abs(pow) <= settings.POWER else settings.POWER * pow / abs (pow)

				print('{}\tSensors: {}\tActual: {} Error: {} PID: {}'.format(
					datetime.now(),
					sensors_data,
					actual,
					settings.STATE_OK - actual,
					pow))

			[l, r] = [settings.LEFT_MOTOR_POWER, settings.RIGHT_MOTOR_POWER]
			
			if pow > 0:
				#l -= int(pow)
				l -= int(pow)
				r += int(pow)
			if pow < 0:
				#r += int(pow)
				l -= int(pow)
				r += int(pow)
			
			print('Power {} {}'.format(l, r))

			lmotor.rotate(True, l)
			rmotor.rotate(True, r)
		else:
			print('{}\tAction: {}'.format(datetime.now(), todo))
			if todo == "stop":
				lmotor.stop()
				rmotor.stop()
			if todo == "90" or todo == "-90":
				lmotor.rotate(todo == "90", settings.LEFT_MOTOR_POWER*1.5)
				rmotor.rotate(todo == "-90", settings.RIGHT_MOTOR_POWER*1.5)
				sleep(0.2)
				lmotor.stop()
				rmotor.stop()
			if todo == "180":
				lmotor.rotate(True, settings.LEFT_MOTOR_POWER*1.5)
				rmotor.rotate(False, settings.RIGHT_MOTOR_POWER*1.5)
				sleep(0.4)
				lmotor.stop()
				rmotor.stop()
			# more complex action required: turn around, crossing etc
			if todo == last_state_action:
				state_action_reps += 1

			if state_action_reps >= settings.STATE_ACTION_REPETITIONS:
				# do an action
				pass

			last_state_action = todo

		sleep(settings.FREQ)
except KeyboardInterrupt:
	pass

if lmotor is not None:
    lmotor.stop()
    lmotor.cleanup()

if rmotor is not None:
    rmotor.stop()
    rmotor.cleanup()

GPIO.cleanup()
