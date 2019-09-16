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
