import RPi.GPIO as GPIO
from time import sleep

pins = [18, 23, 24, 25, 8]

GPIO.setmode(GPIO.BCM)

for pin in pins:
    GPIO.setup(pin,GPIO.IN)

print('Testing line sensors...')
for i in range(10000):
    data = [0]*len(pins)

    for i in range(len(pins)):
        data[i] = GPIO.input(pins[i])

    print(data)
    sleep(0.5)

print('Test finished.')

GPIO.cleanup()
