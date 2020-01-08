import abc
import logging

from .base import PWMController

logger = logging.getLogger(__name__)

class GpioPWM(PWMDevice):
    """GPIO pins subset acting as PWM device.

       Notes:
       This method has the following dependencies:
            sudo apt install pigpio python3-pigpio
            sudo systemctl start pigpiod
    """

    def __init__(self, ref, frequency, pins):
        self.ref = ref
        self.frequency = frequency

        self.logger = logger.getChild(__class__.__name__)

        import pigpio
        self.controller = pigpio.pi()
        # output gpio pin controller
        self.controller.set_mode(pin, pigpio.OUTPUT)

    def __del__(self):
        self.controller.stop()

    def set_pulse_width(self, channel, width):
        self.controller.hardware_PWM(channel, self.frequency, width)
