import misc.settings as settings
from gpiozero import Button, LED
from subprocess import check_call
from subprocess import Popen
from signal import pause
from time import time, sleep
import sys

# constants
dbl_press_time = 0.25  # in seconds
p = None

# global variables
press_time = 0
turning_off = False


def when_held():
    global led
    global turning_off

    # set turn off flag to True so button release doesnt trigger app start
    turning_off = True

    print('Button held. Shutting down.')

    led.blink()
    sleep(3)
    check_call('sudo poweroff ', shell=True)


def when_dbl():
    global p, led

    print('Dbl click detected')
    if p is not None:
        p.terminate()
        p.wait()
        p = None
        print('Process terminated')
        led.off()


def when_released():
    global turning_off
    if turning_off:
        return

    global press_time
    global p, led

    if (time()-press_time) <= dbl_press_time:
        when_dbl()
    else:
        print('Button pressed. Starting process.')
        if p is None:
            p = Popen([sys.executable, '/opt/maze/main.py > robot.log'])
            led.on()
        else:
            print('Button pressed. Sending signal.')
            p.send_signal(SIGUSR1)
            led.off()

    press_time = time()

# create GPIO button. This will init GPIO (takes a few secs)
shut_btn = Button(settings.CTRL_BTN, hold_time=6)

print('GPIO is ready.')

led = LED(settings.CTRL_LED)
led.on()
sleep(3)
led.off()

shut_btn.when_held = when_held
shut_btn.when_released = when_released
pause()
