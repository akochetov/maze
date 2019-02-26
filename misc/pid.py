from time import time
from misc.log import log


class PID:
    def __init__(self, pk, ik, dk, d_fading):
        """Initiates PID with P, I and D coefficients as well
        as current percieved error (0 by default)

        Arguments:
            pk {float} -- P coefficient
            ik {float} -- I coefficient
            dk {float} -- D coefficient
            dk_fading {float} -- how much D error will fade from one
            call to another. 0 means it fades completely

        Keyword Arguments:
            last_error {float} -- current percieved error (default: {0.0})
        """

        self.pk = pk
        self.ik = ik
        self.dk = dk
        self.d_fading = d_fading

        self.reset()

    def reset(self):
        """Resets integral and derivative errors
        """

        self.integral = 0
        self.last_error = 0
        self.first_call = True
        self.derivative = 0

    def __get_time(self):
        """Incapuslated method to calcualte current time in seconds.
        Used in claculating iteration time for Derivative part

        Returns:
            [float] -- Measure of current time in floating point seconds
        """

        return time()

    def get(self, desired_value, actual_value):
        """Calculates output signal with PID

        Arguments:
            desired_value {float} -- Desired value of system state
            actual_value {float} -- Actual current value of system state
        """
        error = desired_value - actual_value

        self.integral = self.integral + error

        if error == 0:
            self.integral = 0

        if self.first_call:
            self.first_call = False
            self.last_error = error

        self.derivative = (
            error - self.last_error + self.derivative * self.d_fading
            )
        self.last_error = error

        log('p: {}\ti: {} d: {}'.format(
            error * self.pk,
            self.integral * self.ik,
            self.derivative * self.dk))

        return (
            self.pk * error +
            self.ik * self.integral +
            self.dk * self.derivative
        )
