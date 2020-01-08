"""PWM channel class 

A pwm channel is calibrated at several points.  These points are mapped to 
that split the range [-1, 1] and intermediate points are determined
by linear interpolation.
"""
import bisect

class PWMChannel:
    def __init__(self, pwm_ref, channel, pulses):
        self.pwm_ref = pwm_ref
        self.channel = channel
        self.pulses = sorted(pulses.items(), key=lambda x: x[1])
        self.values = [-1 + 2 * i / (len(self.pulses) - 1) for i in range(len(self.pulses))]

    def get_value(self, devices):
        pwm_device = devices[self.pwm_ref]
        width = pwm_device.get_pulse_width(channel)
        return self._width2value(width)

    def set_value(self, value, devices):
        width = self._value2width(value)
        pwm_device = devices[self.pwm_ref]
        pwm_device.set_pulse_width(self.channel, width)

    # def _value2width(self, value):
    #     """Converts value to pulse width (s)"""
    #     widths = [w for r, w in self.pulses]
    #     return width

    # def _width2value(self, width):
    #     """Converts pulse width (s) to value [-1, 1]"""
    #     widths = [width for ref, width in self.pulses]
    #     idx = bisect.bisect_left
    #     return value
