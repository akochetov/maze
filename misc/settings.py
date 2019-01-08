# control time interval
FREQ = 1 / 10

# motors config
RIGHT_MOTOR = {"EN": 13,"IN1": 5,"IN2": 6}
LEFT_MOTOR = {"EN": 19,"IN1": 20,"IN2": 16}
POWER = 30
LEFT_MOTOR_POWER = POWER
RIGHT_MOTOR_POWER = POWER
PWM = 30

# line sensors
LINE_SENSORS = [8, 25, 24, 23, 18]

# speed per power in m/sec
POWER_SPEED = {
	30:		0.1,
	100:	0.3}

# tape width in m
TAPE_WIDTH = 0.03

# PID coefficients, PK, IK and DK repsectively
PID = [3, 0, 0.1]#0.1, 0.05]

# state error
STATE_OK = 0

STATE_ERROR = {
	"01111": -4,
	"00011": -3,
	"00111": -3,
	"10111": -2,
	"10011": -1,
	"11011": STATE_OK,
	"11001": 1,
	"11101": 2,
	"11100": 3,
	"11000": 3,
	"11110": 4}

# state actions
STATE_ACTION = {
	"00000": "180 degrees",
	#"11000": "right 90 degrees",
	#"00011": "left 90 degrees",
	"11111": "stop"}

# how many times in a row action has to repeat to account
STATE_ACTION_REPETITIONS = 2
