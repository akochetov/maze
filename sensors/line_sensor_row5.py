"""
Line following IR sensor module, RPi aimed

States table:

State   Interpretation                                  Left motor power in %       Right motor power in %
00100   Straight or Back (if next is 00000)             20                          20
01110   Straight or Back (if next is 00000)             20                          20

01000   Left. Much out of line. Fix required            20                          10
01100   Left. Slightly out of line. Major fix required  20                          15
00010   Right. Much out of line. Fix required           10                          20
00110   Right. Slightly out of line. Fix required       15                          20

10000   Left Crossing.                                  5                           20
11000   Left Crossing.                                  7                           20
11100   Left Crossing.                                  10                          20

00001   Right Crossing.                                 20                          5
00011   Right Crossing.                                 20                          7
00111   Right Crossing.                                 20                          10

11111   T-shaped crossing. Left and Right. Front - ?
00000   Out of line. Decide basing on prev value.        ?                           ?
"""
from line_sensor_source_base import LineSensorSourceBase

