from signal import signal, SIGINT, SIGTERM
import sys
import os
import time
from car import Car
from sensors.line_sensor import LineSensor
import misc.settings as settings

from misc.orientation import Orientation
from worlds.virtual_world import VirtualWorld
from chassis.virtual_chassis import VirtualChassis
from sensors.virtual_line_sensor_source import VirtualLineSensorSource

import RPi.GPIO as GPIO
from chassis.rpi_2wheels_chassis import RPi2WheelsChassis
from sensors.rpi_line_sensor_source import RPiLineSensorSource
from misc.rpi_line_sensor_pid import RPiLineSensorPID

exit_loop = False


def exitLoop(arg1, arg2):
    global exit_loop
    exit_loop = True

signal(SIGINT, exitLoop)
signal(SIGTERM, exitLoop)


GPIO.setmode(GPIO.BCM)

line_sensor = LineSensor(RPiLineSensorSource(
        settings.LINE_SENSORS,
        Orientation.SOUTH,
        invert=True,
        signals_window_size=settings.SIGNALS_WINDOWS_SIZE,
        state_trigger_repetitions=settings.STATE_ACTION_REPETITIONS
        ))

sensor_pid = RPiLineSensorPID(
        settings.PID,
        line_sensor,
        settings.STATE_OK
    )

chassis = RPi2WheelsChassis(
        settings.LEFT_MOTOR,
        settings.RIGHT_MOTOR,
        settings.LEFT_MOTOR_POWER,
        settings.RIGHT_MOTOR_POWER,
        settings.TIME_TO_TURN,
        settings.BRAKE_TIME,
        settings.PWM,
        sensor_pid,
        settings.PID_FREQ)

car = Car(None, chassis, [line_sensor], ORIENTATION)

car.move()
while not exit_loop:
    time.sleep(0.5)

line_sensor.stop()
car.stop()

print('Test finished.')

GPIO.cleanup()
