import RPi.GPIO as GPIO


class PWMMotor:
    _pwm = None

    _pwm_freq = 0

    _enable_pin = 0
    _in1_pin = 0
    _in2_pin = 0

    def __init__(self, enable_pin, in1_pin, in2_pin, pwm_frequency=100):
        GPIO.setmode(GPIO.BCM)

        self._enable_pin = enable_pin
        self._in1_pin = in1_pin
        self._in2_pin = in2_pin
        self._pwm_freq = pwm_frequency

        self.setup()

    def setup(self):
        GPIO.setup(self._enable_pin, GPIO.OUT)
        GPIO.setup(self._in1_pin, GPIO.OUT)
        GPIO.setup(self._in2_pin, GPIO.OUT)

        self._pwm = GPIO.PWM(self._enable_pin, self._pwm_freq)
        self._pwm.start(0)

    def rotate(self, clockwise=True, power=100):
        if clockwise:
            GPIO.output(self._in2_pin, GPIO.LOW)
            GPIO.output(self._in1_pin, GPIO.HIGH)
        else:
            GPIO.output(self._in1_pin, GPIO.LOW)
            GPIO.output(self._in2_pin, GPIO.HIGH)

        self._pwm.ChangeDutyCycle(power)

    def stop(self):
        if self._pwm is not None:
            GPIO.output(self._in1_pin, GPIO.LOW)
            GPIO.output(self._in2_pin, GPIO.LOW)
            self._pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.stop()
        if self._pwm is not None:
            self._pwm.stop()
            self._pwm = None
