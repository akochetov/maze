import RPi.GPIO as GPIO

class LineSensor(object):

	def __init__(self, sensors):
		self.sensors = sensors

	def setup(self):
		for sensor in self.sensors:
			GPIO.setup(sensor,GPIO.IN)
	
	def get_sensors_data(self):
		str_to_ret = ''
		for sensor in self.sensors:
			str_to_ret+=str(GPIO.input(sensor))
		return str_to_ret

