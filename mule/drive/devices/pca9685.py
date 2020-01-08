import logging

from board import SCL, SDA
import busio
import adafruit_pca9685

from .base import PWMDevice

logger = logging.getLogger(__name__)


class PCA9685(PWMDevice):
    """PCA9685 16 Channel 12-bit PWM I2C module.

       This wraps the adafruit_circuitpython_pca9685 library

       Attributes:
            address: device i2c address
            frequency: refresh rate (Hz)
            controller: device class from Adafruit

       Note:
       The adafruit library utilizes 16-bit duty cycle specification and handles
       the conversion to the 12-bit hardware resolution of the device.
    """

    DEFAULT_WIDTH = 0.0015  # 1.5ms

    def __init__(self, ref, address, frequency):
        self.ref = ref
        self.address = address

        i2c_bus = busio.I2C(SCL, SDA)
        self.controller = adafruit_pca9685.PCA9685(i2c_bus,
                                                    address=address)
        self.controller.frequency = frequency

        self.logger = logger.getChild(__class__.__name__)
        self.logger.debug(f'Reference:      {ref}')
        self.logger.debug(f'Address:        0x{address:X}')
        self.logger.debug(f'Frequency (Hz): {frequency}')

    @property
    def frequency(self):
        return self.controller.frequency

    @frequency.setter
    def frequency(self, frequency):
        self.controller.frequency = frequency

    def set_pulse_width(self, channel, width):
        duty_cycle = self._width2ticks(width, self.frequency)
        _channel = self.controller.channels[channel]
        _channel.duty_cycle = duty_cycle

        self.logger.debug(f'Pulse width (s):           {width}')
        self.logger.debug(f'Pulse duty cycle (16-bit): {_channel.duty_cycle}')

    def _width2duty_cycle(self, width, frequency):
        """Converts width (s) to 16-bit ticks."""
        # The adafruit library expects a 16-bit duty cycle tick specification
        # and internally reduces that to 12 bits.
        RESOLUTION = 2**16

        # duty cycle is proportion of 'on' time per period
        duty_cycle_proportion = min(width * frequency, 1.0)
        duty_cycle = int(duty_cycle_proportion * RESOLUTION)
        return duty_cycle
