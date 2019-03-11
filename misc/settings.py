# Virtual or physical maze
VIRTUAL = 0

# Shall we return with shortest path when exit is reached?
NAVIGATE_BACK = 1

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

# Maze time: 35.323312520980835
LEFT_MOTOR_POWER = {"FAST": 39, "SLOW": 15, "TURN": 36}
RIGHT_MOTOR_POWER = {"FAST": 42, "SLOW": 18, "TURN": 42}

PWM = 40

# line sensors pins for digital module
LINE_SENSORS = [12, 11, 8, 25, 24, 23, 18]

# SPI sensor parameters
SPI_LINE_SENSOR_CHANNELs = [0, 1, 2, 3, 4, 5, 6]
SPI_LINE_SENSOR_PARAMS = {"MIN": 500, "MID": 750, "MAX": 1000}

# PID coefficients, PK, IK and DK repsectively, then D fading coefficient
# D fading means that every iteration D error will be multiplied by D fading
# PID = [1 / 125, 0, 1 / 9]
PID = [1 / 135, 0, 1 / 12, 0.10]

# state error
STATE_OK = 3000

# how many times in a row action has to repeat to count
SIGNALS_WINDOWS_SIZE = 20
STATE_ACTION_REPETITIONS = 5

# maze map settings
TIME_ERROR = 0.4
TIME_TO_TURN = 0.32
BRAKE_TIME = 1.0 / 12.0

# if we have turn very early afte previous one - bounce back (ignore it)
TURN_BOUNCE_TIME = 1.0
