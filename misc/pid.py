from time import time


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

        self.integral = 0
        self.last_error = last_error
        self.before_last_error = last_error

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
        self.integral = self.integral + (error * iteration)
        derivative = (error - self.before_last_error) / iteration

        if self.last_error != error:
            self.error_before_last = self.last_error
            self.last_error = error
            self.reset_time()

        return
        self.pk * error
        + self.ik * self.integral
        + self.dk * derivative
