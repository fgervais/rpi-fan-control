class Fan:
    def __init__(self, pigpio_pi, pwm_pin):
        self.pigpio_pi = pigpio_pi
        self.pwm_pin = pwm_pin

    @property
    def speed(self):
        duty_cycle = self.pigpio_pi.get_PWM_dutycycle(self.pwm_pin)
        return (1e6 - duty_cycle) / 1e6

    @speed.setter
    def speed(self, speed):
        multiplier = 1 - speed
        self.pigpio_pi.hardware_PWM(
            self.pwm_pin,
            25000,
            int(1e6*multiplier))


class Controller:
    def __init__(self, config):
        self.config = config

    def required_speed(self, temperature):
        low_boundary = None
        high_boundary = None

        for i in self.config:
            if temperature > i["t"]:
                low_boundary = i
            else:
                high_boundary = i
                break

        if low_boundary is None:
            return 0
        if high_boundary is None:
            return 100

        req_speed_pct = (low_boundary["speed"]
                + (temperature - low_boundary["t"])
                * (high_boundary["speed"] - low_boundary["speed"])
                / (high_boundary["t"] - low_boundary["t"]))
        return round(req_speed_pct / 100, 2)
