# Virtual or physical maze
VIRTUAL = 1

# Logging
LOG = 1

# control iterations per second
FREQ = 20

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}
POWER = 35
LEFT_MOTOR_POWER = POWER
RIGHT_MOTOR_POWER = POWER+1
PWM = 25

# line sensors
LINE_SENSORS = [8, 25, 24, 23, 18]

# speed per power in m/sec
POWER_SPEED = {
    30:        0.1,
    100:    0.3}

# tape width in m
TAPE_WIDTH = 0.03

# PID coefficients, PK, IK and DK repsectively
PID = [4, 1.5, 1]  # this quite worked

# state error
STATE_OK = 0

STATE_ERROR = {
    "10000": -3,
    # "00011": -3,
    "11000": -2,
    "01000": -1.5,
    "01100": -1,
    "00100": STATE_OK,
    "00110": 1,
    "00010": 1.5,
    "00011": 2,
    # "11000": 3,
    "00001": 3}

# state actions
STATE_ACTION = {
    "11100": 90,
    "00111": -90,
    "11111": 180}

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 10
STATE_ACTION_REPETITIONS = 3

# maze map settings
TIME_ERROR = 0.5  # / 2
TIME_TO_TURN = 0.8
