from time import time


class PID:
    def __init__(self, pk, ik, dk, last_error=0):
        self.pk = pk
        self.ik = ik
        self.dk = dk
        #self.iteration_time = iteration_time

        self.integral = 0
        self.last_error = last_error
        self.before_last_error = last_error

        self.reset_time()

    def reset_time(self):
        self.iteration_time = self.get_time()

    def get_time(self):
        return time()

    def get(self, desired_value, actual_value):
        iteration = self.get_time() - self.iteration_time

        error = desired_value - actual_value
        self.integral = self.integral + (error * iteration)
        derivative = (error - self.before_last_error) / iteration

        if self.last_error != error:
            self.error_before_last = self.last_error
            self.last_error = error
            self.reset_time()

        return self.pk * error + self.ik * self.integral + self.dk * derivative# + bias
