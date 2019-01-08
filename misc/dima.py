import RPi.GPIO as GPIO
from time import sleep
from pwm_motor import PWMMotor

freq = 1/30
pow = 30

lm = {"EN":13,"IN1":5,"IN2":6}
rm = {"EN":19,"IN1":20,"IN2":16}

sensors = [18,23,24,25,8]
states = {'11111':[0,0],
          '00000':[0,0],
          '11011':[pow,pow],
          '10111':[pow-7,pow+2],
          '10011':[pow-5,pow+5],
          '01111':[pow-25,pow+10],
          '00111':[pow-25,pow+10],
          '11101':[pow+2,pow-7],
          '11001':[pow+0,pow-5],
          '11110':[pow+10,pow-15],
          '11100':[pow+10,pow-15],
          '00011':[pow-15,pow+10],
          '10001':[pow,pow],
          '11000':[pow+10,pow-25],
          '10000':[pow+10,pow-25],
          '00001':[pow-15,pow+10],
          }


def get_sensors_data(sensors):
    str_to_ret = ''
    for sensor in sensors:
        str_to_ret+=str(GPIO.input(sensor))
    return str_to_ret


def get_state(sensors_data):
    if sensors_data in states:
        return states[sensors_data]

    return [0,0]

GPIO.setmode(GPIO.BCM)

lmotor = None
rmotor = None
try:
    lmotor = PWMMotor(*lm.values(),pwm_frequency=20)
    rmotor = PWMMotor(*rm.values(),pwm_frequency=20)
    lmotor.setup()
    rmotor.setup()

    for sensor in sensors:
        GPIO.setup(sensor,GPIO.IN)

    while True:
        sensors_data = get_sensors_data(sensors)
        [l, r] = get_state(sensors_data)

        if sensors_data != '00000' and sensors_data != '11111':
            print('Sensors: {}\tPower {} {}'.format(sensors_data, l, r))

        lmotor.rotate(True, l)
        rmotor.rotate(True, r)

        sleep(freq)
except KeyboardInterrupt:
    pass

if lmotor is not None:
    lmotor.stop()
    lmotor.cleanup()

if rmotor is not None:
    rmotor.stop()
    rmotor.cleanup()

GPIO.cleanup()