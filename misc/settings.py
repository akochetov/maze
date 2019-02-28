# Virtual or physical maze
VIRTUAL = 0

# Shall we return with shortest path when exit is reached?
NAVIGATE_BACK = 0

# Logging
LOG = 0

# control iterations per second
CTRL_FREQ = 80
PID_FREQ = 27

# button and LED pins to control robot
CTRL_BTN = 14
CTRL_LED = 15

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}

LEFT_MOTOR_POWER = {"FAST": 30, "SLOW": 18, "TURN": 26}
RIGHT_MOTOR_POWER = {"FAST": 34, "SLOW": 22, "TURN": 30}

PWM = 50

# line sensors
LINE_SENSORS = [12, 11, 8, 25, 24, 23, 18]

# PID coefficients, PK, IK and DK repsectively, then D fading coefficient
# D fading means that every iteration D error will be multiplied by D fading
# PID = [1 / 125, 0, 1 / 9]
PID = [1 / 130, 0, 1 / 14, 0.15]

# state error
STATE_OK = 3000

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 20
STATE_ACTION_REPETITIONS = 5

# maze map settings
TIME_ERROR = 1.0
TIME_TO_TURN = 0.38
BRAKE_TIME = 1.0 / 17.0

# if we have turn very early afte previous one - bounce back (ignore it)
TURN_BOUNCE_TIME = 1.0
