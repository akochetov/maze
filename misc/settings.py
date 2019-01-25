# Virtual or physical maze
VIRTUAL = 0

# Logging
LOG = 1

# control iterations per second
FREQ = 20

# button and LED pins to control robot
CTRL_BTN = 14
CTRL_LED = 15

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}

LEFT_MOTOR_POWER = {"FAST": 80, "SLOW": 40, "TURN": 80}
RIGHT_MOTOR_POWER = {"FAST": 81, "SLOW": 41, "TURN": 81}

PWM = 25

# line sensors
LINE_SENSORS = [8, 25, 24, 23, 18]

# PID coefficients, PK, IK and DK repsectively
PID = [4, 1.5, 1]

# state error
STATE_OK = 0

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 10
STATE_ACTION_REPETITIONS = 3

# maze map settings
TIME_ERROR = 0.5  # / 2
TIME_TO_TURN = 0.8
