# Virtual or physical maze
VIRTUAL = 0

# Shall we return with shortest path when exit is reached?
NAVIGATE_BACK = 0

# Logging
LOG = 1

# control iterations per second
CTRL_FREQ = 100
PID_FREQ = 40

# button and LED pins to control robot
CTRL_BTN = 14
CTRL_LED = 15

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}

LEFT_MOTOR_POWER = {"FAST": 28, "SLOW": 28, "TURN": 28}
RIGHT_MOTOR_POWER = {"FAST": 33, "SLOW": 33, "TURN": 34}

PWM = 40

# line sensors
LINE_SENSORS = [12, 11, 8, 25, 24, 23, 18]
# LINE_SENSORS = [8, 25, 24, 23, 18]

# PID coefficients, PK, IK and DK repsectively
PID = [1 / 130, 0, 1 / 8.5]

# state error
STATE_OK = 3000

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 30
STATE_ACTION_REPETITIONS = 5

# maze map settings
TIME_ERROR = 0.5  # / 2
TIME_TO_TURN = 1
BRAKE_TIME = 1.0 / 14.0
