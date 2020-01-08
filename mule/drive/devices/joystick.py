"""Joystick device driver."""

import logging
import struct

import yaml


class JoystickDevice:
    """Hardware interface to joystick

    Attributes:
    joystick
    ref
    device_path
    event_types
    axes
    buttons


    Notes:
    See: https://www.kernel.org/doc/html/v4.16/input/joydev/joystick-api.html

    This object opens the device in blocking mode.  This means that the read 
    operation will block the thread on which it is running until it registers an
    event.  As a result, this device must definitely be controlled by a threaded
    part.
    See:
    https://www.kernel.org/doc/html/v4.16/input/joydev/joystick-api.html#reading
    One could open the device in non-blocking mode, but this comes with its own
    headaches (as a queue of events needs then to be processed) and probably 
    does not make sense for this use case.
    """
    def __init__(self, ref, device_path, event_types, axes, buttons):
        self.ref = ref
        self.device_path = device_path
        self.event_types = event_types
        self.axes = axes
        self.buttons = buttons

    def open(self):
        self.joystick = open(self.device_path, 'rb')

    def close(self):
        self.joystick.close()

    def poll(self):
        ''' Polls joystick device for events.

            The returned event is either None or an 8B structure comprising:
                I (unsigned int)  4B timestamp in milliseconds
                h (signed short)  2B event value
                B (unsigned char) 1B event type
                B (unsigned char) 1B event key

            event values are:
                {0, 1} for buttons
                [-MAX_AXIS_VALUE, MAX_AXIS_VALUE] for axes

            There are three event types: init, button, axis

            The event keys indicate the particular button/axis that triggered
            the event.
        '''
        # in principle a signed short is a 16-bit entity ranging from -32768 to 
        # 32767 but the documentation for the linux joystick api at
        # https://www.kernel.org/doc/html/v4.16/input/joydev/joystick-api.html
        # states that only values [-32767,32767] are emitted
        MAX_AXIS_VALUE = 32767

        # event reference and value
        ref = None
        value = None

        event = self.joystick.read(8)

        if event:
            timestamp, event_value, event_type, event_key = struct.unpack(
                'IhBB', event)

            if event_type & self.event_types['init']:
                pass

            elif event_type & self.event_types['axis']:
                ref = self.axes[event_key]
                value = event_value / MAX_AXIS_VALUE

            elif event_type & self.event_types['button']:
                ref = self.buttons[event_key]
                value = event_value

            else:
                pass

        return ref, value
