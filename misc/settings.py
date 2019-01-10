# control time interval
FREQ = 1 / 20

# motors config
RIGHT_MOTOR = {"EN": 13,"IN1": 5,"IN2": 6}
LEFT_MOTOR = {"EN": 19,"IN1": 20,"IN2": 21}
POWER = 40
LEFT_MOTOR_POWER = POWER
RIGHT_MOTOR_POWER = POWER+1
PWM = 40

# line sensors
LINE_SENSORS = [8, 25, 24, 23, 18]

# speed per power in m/sec
POWER_SPEED = {
	30:		0.1,
	100:	0.3}

# tape width in m
TAPE_WIDTH = 0.03

# PID coefficients, PK, IK and DK repsectively
PID = [5, 0, 5.5]#0.1, 0.05]

# state error
STATE_OK = 0

STATE_ERROR = {
	"01111": -3,
	#"00011": -3,
	"00111": -2,
	"10111": -1.5,
	"10011": -0.5,
	"11011": STATE_OK,
	"11001": 0.5,
	"11101": 1.5,
	"11100": 2,
	#"11000": 3,
	"11110": 3}

# state actions
STATE_ACTION = {
	"00000": "stop",
	"11000": "90",
	"00011": "-90",
	"11111": "180"}

# how many times in a row action has to repeat to account
STATE_ACTION_REPETITIONS = 2
