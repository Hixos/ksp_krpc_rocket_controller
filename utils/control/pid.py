
class PIDController:

    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.integral = 0
        self.last_error = 0
        self.setpoint = 0

        self.is_integral_limited = False
        self.integral_limit = 0

    def setSetpoint(self, setpoint):
        self.setpoint = setpoint

    def resetIntegral(self):
        self.integral = 0

    def setIntegralLimit(self, limit):
        self.is_integral_limited = True
        self.integral_limit = abs(limit)

    def removeIntegralLimit(self):
        self.is_integral_limited = False

    def update(self, value, dt):
        error = value - self.setpoint

        self.integral += error * dt

        if self.is_integral_limited:
            self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)

        derivative = (error - self.last_error)/dt

        self.last_error = error

        return error*self.Kp + self.integral*self.Ki + derivative*self.Kd
