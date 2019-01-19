from time import time
from datetime import datetime


class PID:
    def __init__(self, pk, ik, dk, last_error=0.0):
        """Initiates PID with P, I and D coefficients as well
        as current percieved error (0 by default)

        Arguments:
            pk {float} -- P coefficient
            ik {float} -- I coefficient
            dk {float} -- D coefficient

        Keyword Arguments:
            last_error {float} -- current percieved error (default: {0.0})
        """

        self.pk = pk
        self.ik = ik
        self.dk = dk

        # print('PID was setup {} {} {}'.format(pk, ik, dk))

        self.integral = 0
        self.last_error = last_error
        self.before_last_error = last_error
        self.first_call = True
        self.reset_time()

    def reset_time(self):
        """Starts new iteration time measuring for further
        Derivative part calculations
        """

        self.iteration_time = self.__get_time()

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

        iteration = self.__get_time() - self.iteration_time

        error = desired_value - actual_value

        if self.first_call:
            self.before_last_error = error
            self.first_call = False

        if actual_value == desired_value:
            # experimental - reducing I part as we drive forward correctly
            self.integral = self.integral / 2
        else:
            self.integral = self.integral + (error * iteration)

        derivative = (error - self.before_last_error) / iteration

        # experimental - reducing D part every iteration
        self.before_last_error += (error - self.before_last_error) / 4

        if self.last_error != error:
            self.before_last_error = self.last_error
            self.last_error = error
            self.reset_time()

        print('{}\tp: {}\ti: {} d: {}'.format(
            datetime.now(),
            error,
            self.integral,
            derivative))

        return self.pk * error + self.ik * self.integral + self.dk * derivative
