import abc

class PWMDevice(abc.ABC):
    @abc.abstractproperty
    def frequency(self):
        """Refresh rate of controller"""

    @frequency.setter
    @abc.abstractmethod
    def frequency(self, frequency):
        """Set refresh rate of controller"""

    @abc.abstractmethod
    def set_pulse_width(self, channel, width):
        """Set pulse width on channel in seconds"""
