from line_sensor_source_base import LineSensorSourceBase
import RPi.GPIO as GPIO

PINS = 5
class RPiLineSensorSource(LineSensorSourceBase):
    '''
    RPi implementation of digital line sensor with 5 IRs in line
    '''

	def __init__(self, sensors):
		self.sensors = sensors

		self.setup()

	def setup(self):
		for sensor in self.sensors:
			GPIO.setup(sensor,GPIO.IN)
	
	def get_sensors_data(self):
		str_to_ret = ''
		for sensor in self.sensors:
			str_to_ret+=str(GPIO.input(sensor))
		return str_to_ret