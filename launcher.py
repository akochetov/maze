import misc.settings as settings
import RPi.GPIO as GPIO
from subprocess import check_call
from subprocess import Popen
from signal import pause
from time import time, sleep
import sys
from threading import Thread

# constants
hold_timeout = 6  # seconds
button_back_timeout = 10  # seconds
dbl_press_time = 0.25  # in seconds
p = None
down = 0

# global variables
press_time = 0
dbl = False
turning_off = False


class BtnThread(Thread):
    def __init__(self, timeout, callback, continuous=False):
        super().__init__()
        self.timeout = timeout
        self.callback = callback
        self.alive = False
        self.continuos = continuous

    def run(self):
        self.alive = True
        self.started = time()
        while self.alive:
            sleep(0.01)

            if time() - self.started > self.timeout:
                if self.continuos:
                    self.started = time()
                else:
                    self.stop()
                self.callback()

    def stop(self):
        self.alive = False


def led_on():
    GPIO.output(settings.CTRL_LED, GPIO.HIGH)


def led_off():
    GPIO.output(settings.CTRL_LED, GPIO.LOW)


def led_blink():
    for i in range(5):
        GPIO.output(settings.CTRL_LED, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(settings.CTRL_LED, GPIO.LOW)
        sleep(0.5)


def on_held():
    global turning_off

    # set turn off flag to True so button release doesnt trigger app start
    turning_off = True

    print('Button held. Shutting down...')

    setup_button()
    led_blink()
    check_call('sudo poweroff ', shell=True)


def on_dbl():
    global p, hold_thread

    print('Dbl click detected')
    hold_thread.stop()
    if p is not None:
        p.terminate()
        p.wait()
        p = None
        print('Process terminated')
        setup_button()
        led_on()
        sleep(1)
        led_off()


def on_pressed():
    global p, turning_off, button_thread, hold_thread

    if turning_off:
        return

    print('Button pressed')
    hold_thread.stop()
    if p is None:
        p = Popen([sys.executable, '/opt/maze/main.py'])
        button_thread = BtnThread(button_back_timeout, setup_button)
        button_thread.start()


def on_edge(channel):
    global press_thread, hold_thread, press_time, dbl, down
    input = GPIO.input(channel)

    if input == GPIO.LOW:
        print('Btn down')
        press_thread.stop()
        if not hold_thread.alive:
            hold_thread = BtnThread(hold_timeout, on_held)
            hold_thread.start()
        if time()-press_time < dbl_press_time:
            on_dbl()
            dbl = True
        press_time = time()
    else:
        print('Btn up')
        hold_thread.stop()
        if not press_thread.alive and not dbl:
            press_thread = BtnThread(dbl_press_time * 2, on_pressed)
            press_thread.start()
        else:
            press_thread.stop()
        dbl = False


def setup_button():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings.CTRL_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.remove_event_detect(settings.CTRL_BTN)
    GPIO.add_event_detect(settings.CTRL_BTN, GPIO.BOTH)
    GPIO.add_event_callback(settings.CTRL_BTN, on_edge)
    GPIO.setup(settings.CTRL_LED, GPIO.OUT)
    led_off()


print('GPIO is ready.')

hold_thread = BtnThread(hold_timeout, on_held)
press_thread = BtnThread(dbl_press_time * 2, on_pressed)
button_thread = BtnThread(button_back_timeout, setup_button)
setup_button()
led_on()
sleep(3)
led_off()

pause()
