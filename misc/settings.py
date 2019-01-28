# Virtual or physical maze
VIRTUAL = 0

# Logging
LOG = 1

# control iterations per second
FREQ = 50

# button and LED pins to control robot
CTRL_BTN = 14
CTRL_LED = 15

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}

LEFT_MOTOR_POWER = {"FAST": 50, "SLOW": 25, "TURN": 50}
RIGHT_MOTOR_POWER = {"FAST": 50, "SLOW": 25, "TURN": 50}

PWM = 40

# line sensors
LINE_SENSORS = [12, 7, 8, 25, 24, 23, 18]
# LINE_SENSORS = [8, 25, 24, 23, 18]

# PID coefficients, PK, IK and DK repsectively
PID = [1 / 100, 1 / 200, 1 / 500]
# PID = [1 / 150, 1 / 15000, 1 / 500]

# state error
STATE_OK = 3000

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 20
STATE_ACTION_REPETITIONS = 3

# maze map settings
TIME_ERROR = 0.5  # / 2
TIME_TO_TURN = 0.8
BRAKE_TIME = 1.0 / 15.0
