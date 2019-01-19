# Logging
LOG = True

# control time interval
FREQ = 1 / 20

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}
POWER = 40
LEFT_MOTOR_POWER = POWER
RIGHT_MOTOR_POWER = POWER+1
PWM = 20

# line sensors
LINE_SENSORS = [8, 25, 24, 23, 18]

# speed per power in m/sec
POWER_SPEED = {
    30:        0.1,
    100:    0.3}

# tape width in m
TAPE_WIDTH = 0.03

# PID coefficients, PK, IK and DK repsectively
PID = [4, 1.5, 1]

# state error
STATE_OK = 0

STATE_ERROR = {
    "[1, 0, 0, 0, 0]": -3,
    # "00011": -3,
    "[1, 1, 0, 0, 0]": -2,
    "[0, 1, 0, 0, 0]": -1.5,
    "[0, 1, 1, 0, 0]": -1,
    "[0, 0, 1, 0, 0]": STATE_OK,
    "[0, 0, 1, 1, 0]": 1,
    "[0, 0, 0, 1, 0]": 1.5,
    "[0, 0, 0, 1, 1]": 2,
    # "11000": 3,
    "[0, 0, 0, 0, 1]": 3}

# state out
STATE_OUT = "[0, 0, 0, 0, 0]"

# state actions
STATE_ACTION = {
    STATE_OUT: 0,
    "[1, 1, 1, 0, 0]": 90,
    "[0, 0, 1, 1, 1]": -90,
    "[1, 1, 1, 1, 1]": 180}

# how many times in a row action has to repeat to count
STATE_ACTION_REPETITIONS = 2

# maze map settings
TIME_ERROR = 0.25  # / 2
TIME_TO_TURN = 0.4
