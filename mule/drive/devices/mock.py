import abc
import logging

from .base import PWMDevice

logger = logging.getLogger(__name__)

class MockPWMDevice(PWMDevice):
    """A mock pwm device for developers"""
    def set_pulse_width(self, channel, width):
        pass

    def reset_pulse_width(self, channel):
        pass


