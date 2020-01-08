import functools
import logging
import math
import time

from mule.drive.parts.base import BasePart

# TODO: should we really have separate instances for the steering and throttle
#       on the same board
# TODO: check that _signal2pulse allows for the fact that the user may put
#       full_left_pulse < full_right_pulse or
#       full_reverse_pulse > full_forward_pulse
# TODO: document the above idiosyncracy


def _signal2level(signal_ext1, signal_ext2, level_ext1, level_ext2, signal):
    """Linearly transforms signal from signal-space to level-space

       signal_ext1, signal_ext2: float
           limits (in principle) for signal values

       level_ext1, level_ext2: int
           limits for level values (discovered during callibration)

       signal: float
           value to be linearly transformed
    """
    slope = (level_ext2 - level_ext1) / (signal_ext2 - signal_ext1)
    level = slope * (signal - signal_ext1) + level_ext1

    return int(math.floor(level + 0.5))


class SteeringController(BasePart):
    """Controls vehicle steering"""

    input_keys = ('steering_signal', )
    output_keys = ()

    def __init__(self, device, channel, straight_level, full_left_level,
                 full_right_level, full_left_signal, full_right_signal):

        self.device = device
        self.channel = channel

        self.straight_level = straight_level
        self.full_left_level = full_left_level
        self.full_right_level = full_right_level

        self.full_left_signal = full_left_signal
        self.full_right_signal = full_right_signal

    def from_config(cls, device, config):
        raise NotImplementedError

    def start(self):
        pass

    def transform(self, state):
        """Send signal as level pulse to servo"""
        #print(state['steering_signal'])
        level = _signal2level(self.full_left_signal, self.full_right_signal,
                              self.full_left_level, self.full_right_level,
                              state['steering_signal'])

        #print("SteeringController.transform() pulse:", pulse)

        self.device.set_level(self.channel, level)

    def stop(self):
        """Signal the servo to return to straight trajectory"""
        self.device.set_level(self.channel, self.straight_level)

    def __str__(self):
        return (
            f'Steering controller connected to device {repr(self.device)} ' +
            f'on channel {self.channel}')

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(device={repr(self.device)}, ' +
            f'channel={self.channel}, ' +
            f'straight_level={self.straight_level}, ' +
            f'full_left_level={self.full_left_level}, ' +
            f'full_right_level={self.full_right_level}, ' +
            f'full_left_signal={self.full_left_signal}, ' +
            f'full_right_signal={self.full_right_signal}' + ')')


class ThrottleController(BasePart):
    ''' Controls vehicle throttle '''

    input_keys = ('throttle_signal', )
    output_keys = ()

    def __init__(self, device, channel, stopped_level, full_forward_level,
                 full_reverse_level, stopped_signal, full_forward_signal,
                 full_reverse_signal):

        self.device = device
        self.channel = channel

        self.stopped_level = stopped_level
        self.full_forward_level = full_forward_level
        self.full_reverse_level = full_reverse_level

        self.stopped_signal = stopped_signal
        self.full_forward_signal = full_forward_signal
        self.full_reverse_signal = full_reverse_signal

    def from_config(cls, device, config):
        raise NotImplementedError


    def start(self):
        """Calibrate by sending stop signal"""
        self.device.set_level(self.channel, self.stopped_signal)
        time.sleep(0.5)

    def transform(self, state):
        """Send signal as pulse level to servo"""
        if state['throttle_signal'] > self.stopped_signal:
            level = _signal2level(self.stopped_signal,
                                  self.full_forward_signal, 
                                  self.stopped_level,
                                  self.full_forward_level,
                                  state['throttle_signal'])
        else:
            level = _signal2level(self.full_reverse_signal,
                                  self.stopped_signal, 
                                  self.full_reverse_level,
                                  self.stopped_level, 
                                  state['throttle_signal'])

        self.device.set_level(self.channel, level)

    def stop(self):
        ''' Signal to stop vehicle '''
        self.device.set_level(self.channel, self.stopped_level)

    def __str__(self):
        return (
            f'Throttle controller connected to device {repr(self.device)} ' +
            f'on channel {self.channel}')

    def __repr__(self):
        return (f'{self.__class__.__name__}(device={repr(self.device)}, ' +
                f'channel={self.channel}, ' +
                f'stopped_level={self.stopped_level}, ' +
                f'full_forward_level={self.full_forward_level}, ' +
                f'full_reverse_level={self.full_reverse_level}, ' +
                f'stopped_signal={self.stopped_signal}, ' +
                f'full_forward_signal={self.full_forward_signal}, ' +
                f'full_reverse_signal={self.full_reverse_signal}' + ')')
