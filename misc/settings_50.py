# Virtual or physical maze
VIRTUAL = 0

# Shall we return with shortest path when exit is reached?
NAVIGATE_BACK = 1

# Logging
LOG = 0

# control iterations per second
CTRL_FREQ = 150
PID_FREQ = 27

# button and LED pins to control robot
CTRL_BTN = 14
CTRL_LED = 15

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}

LEFT_MOTOR_POWER = {"FAST": 51, "SLOW": 39, "TURN": 58}
RIGHT_MOTOR_POWER = {"FAST": 54, "SLOW": 42, "TURN": 54}

PWM = 50

# line sensors pins for digital module
LINE_SENSORS = [12, 11, 8, 25, 24, 23, 18]

# PID coefficients, PK, IK and DK repsectively, then D fading coefficient
# D fading means that every iteration D error will be multiplied by D fading
# PID = [1 / 125, 0, 1 / 9]
PID = [1 / 135, 0, 1 / 13, 0.10]

# state error
STATE_OK = 3000

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 30
STATE_ACTION_REPETITIONS = 5

# maze map settings
TIME_ERROR = 0.5
TIME_TO_TURN = 0.38
BRAKE_TIME = 1.0 / 8.0

# if we have turn very early afte previous one - bounce back (ignore it)
TURN_BOUNCE_TIME = 1.0
