# Virtual or physical maze
VIRTUAL = 0

# Shall we return with shortest path when exit is reached?
NAVIGATE_BACK = 0

# Logging
LOG = 0

# control iterations per second
CTRL_FREQ = 100
PID_FREQ = 100

# button and LED pins to control robot
CTRL_BTN = 14
CTRL_LED = 15

# motors config
RIGHT_MOTOR = {"EN": 13, "IN1": 5, "IN2": 6}
LEFT_MOTOR = {"EN": 19, "IN1": 20, "IN2": 21}

# Maze time: 27.54425597190857
LEFT_MOTOR_POWER = {"FAST": 75, "SLOW": 10, "TURN": 75}
RIGHT_MOTOR_POWER = {"FAST": 84, "SLOW": 15, "TURN": 84}

PWM = 25

# sensor types
SENSOR_SPI = "SPI"
SENSOR_GPIO = "GPIO"
SENSOR_TYPE = SENSOR_SPI

# line sensors pins for digital module
LINE_SENSORS = [12, 11, 8, 25, 24, 23, 18]

# SPI sensor parameters
SPI_LINE_SENSOR_CHANNELS = [0, 1, 2, 3, 4, 5, 6]
SPI_LINE_SENSOR_MIN_MAX = [
    {"MIN": 855, "MAX": 990},
    {"MIN": 855, "MAX": 990},
    {"MIN": 855, "MAX": 990},
    {"MIN": 855, "MAX": 990},
    {"MIN": 850, "MAX": 990},
    {"MIN": 850, "MAX": 990},
    {"MIN": 850, "MAX": 990}
    ]

# PID coefficients, PK, IK and DK repsectively, then D fading coefficient
# D fading means that every iteration D error will be multiplied by D fading
PID = [1 / 25, 1 / 10000, 1 / 2.45, 0]

# state error
STATE_OK = 2000

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 20
STATE_ACTION_REPETITIONS = 3

# maze map settings
TIME_ERROR = 0.15
TIME_TO_TURN = 0.2
BRAKE_TIME = 1.0 / 80.0

# if we have turn very early afte previous one - bounce back (ignore it)
TURN_BOUNCE_TIME = 0.3
