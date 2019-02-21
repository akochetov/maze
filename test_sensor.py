import RPi.GPIO as GPIO
from sensors.line_sensor import LineSensor
from sensors.rpi_line_sensor_source import RPiLineSensorSource
from misc.orientation import Orientation
import misc.settings as settings
from time import sleep

GPIO.setmode(GPIO.BCM)

line_sensor = LineSensor(RPiLineSensorSource(
        settings.LINE_SENSORS,
        Orientation.SOUTH,
        invert=True,
        signals_window_size=settings.SIGNALS_WINDOWS_SIZE,
        state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS
        ),
        settings.FREQ)

print('Testing line sensors. Move sensor line above the line to see readings:')
for i in range(10000):
    data = line_sensor.get_state()

    print(bin(data))
    sleep(0.5)

print('Test finished.')

GPIO.cleanup()
