from line_sensor_source_base import LineSensorSourceBase
import RPi.GPIO as GPIO

PINS = 5
class RPiLineSensorRow5(LineSensorSourceBase):
    '''
    RPi implementation of digital line sensor with 5 IRs in line
    '''
    
    def __init__(self, pin1, pin2, pin3, pin4, pin5):
        super().__init__()

        GPIO.setmode(GPIO.BCM)

        self.pins = [pin1, pin2, pin3, pin4, pin5]
        self.state = [0]*PINS
        self.setup()

    def setup(self):
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN)	
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.edge_detected)

    def get_state(self):
        ret = [0] * PINS

        for i in range(PINS):
            ret[i] = int(GPIO.input(self.pins[i]))

        return ret

    def edge_detected(self, pin):
        new_state = self.get_state()

        for i in range(PINS):
            if self.state[i] != new_state[i]:
                self.state = new_state
                trigger_state_change()
                break
 