import math

import titration.utils.constants as constants


class Stir_Control:
    def __init__(
        self,
        pwm_pin,
        duty_cycle=constants.STIR_DUTY_CYCLE,
        frequency=constants.STIR_FREQUENCY,
        debug=False,
    ):
        self.duty_cycle = 0
        self.debug = debug

    def set_motor_speed(self, target, gradual=False):
        if gradual is True:
            direction = math.copysign(1, target - self.duty_cycle)

            # It won't move under 1000, so this speeds up the process
            if direction == 1 and self.duty_cycle < 1000:
                self.duty_cycle = 1000
                if self.debug:
                    print("Stirrer set to {0:.0f}".format(self.duty_cycle))

            while self.duty_cycle != target:
                next_step = min(abs(target - self.duty_cycle), 100)
                self.duty_cycle = self.duty_cycle + (next_step * direction)
                if self.debug:
                    print("Stirrer set to {0:.0f}".format(self.duty_cycle))
        else:
            self.duty_cycle = target
            if self.debug:
                print("Stirrer set to {0:.0f}".format(self.duty_cycle))

    def motor_speed_fast(self):
        self.set_motor_speed(constants.STIR_PWM_FAST, gradual=True)

    def motor_speed_slow(self):
        self.set_motor_speed(constants.STIR_PWM_SLOW, gradual=True)

    def motor_stop(self):
        self.set_motor_speed(0)
