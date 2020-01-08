"""Python wrapper for _jsio joystick extension module.

This module loads commands, axes and buttons. All these are defined in the 
Raspbian linux source at linux/joystick.h. However, not all can be read
explicitly and reference other files within the system source code:
    - asm-generic/ioctl.h
    - asm-generic/ll64.h
    - linux/input-event-codes.h

Here 'CG' stands for 'Command Get'.
"""

import array
import fcntl
import logging


logger = logging.getLogger(__name__)

try:
    logger.debug('Loading _jsio extension module')

    from .ext._jsio import (
        load_JSIOCGAXES, load_JSIOCGBUTTONS, load_JSIOCGNAME, load_JSIOCGAXMAP,
        load_JSIOCGBTNMAP, 
        load_JS_EVENT_AXIS, load_JS_EVENT_BUTTON, load_JS_EVENT_INIT,
        load_MAX_NR_AXES, load_MAX_NR_BUTTONS, load_BTN_MISC)

except ImportError:
    logger.debug('_jsio import failed. Hard-coded events used.')

    def load_JS_EVENT_BUTTON():
        return 0x01

    def load_JS_EVENT_AXIS():
        return 0x02

    def load_JS_EVENT_INIT():
        return 0x80

    def load_JSIOCGAXES():
        return 0x80016a11

    def load_JSIOCGBUTTONS():
        return 0x80016a12

    def load_JSIOCGNAME(name_length):
        SIZESHIFT = 16
        return 0x80006a13 + (name_length << SIZESHIFT)

    def load_JSIOCGAXMAP():
        return 0x80406a32

    def load_JSIOCGBTNMAP():
        return 0x84006a34

    def load_MAX_NR_AXES():
        return 0x40

    def load_MAX_NR_BUTTONS():
        return 0x200

    def load_BTN_MISC():
        return 0x100



def load_device_name(joystick):
    """Load device name of the joystick device"""
    MAX_NAME_LENGTH = 128
    JSIOCGNAME = load_JSIOCGNAME(MAX_NAME_LENGTH)
    container = array.array('B', [0] * MAX_NAME_LENGTH)
    fcntl.ioctl(joystick, JSIOCGNAME, container)
    device_name = container.tobytes().decode('utf-8')
    return device_name


def load_event_types():
    """Load init, button and axis event type codes"""
    event_types = {}
    event_types['button'] = load_JS_EVENT_BUTTON()
    event_types['axis'] = load_JS_EVENT_AXIS()
    event_types['init'] = load_JS_EVENT_INIT()
    return event_types


def load_nr_axes(joystick):
    """Load number of axes recognized for the device"""
    JSIOCGAXES = load_JSIOCGAXES()
    container = array.array('B', [0])
    fcntl.ioctl(joystick, JSIOCGAXES, container)
    nr_axes = container[0]

    return nr_axes


def load_nr_buttons(joystick):
    """Load number of buttons recognized for the device"""
    JSIOCGBUTTONS = load_JSIOCGBUTTONS()
    container = array.array('B', [0])
    fcntl.ioctl(joystick, JSIOCGBUTTONS, container)
    nr_buttons = container[0]

    return nr_buttons


def load_axes_event_codes(joystick):
    """Load axes input event codes"""
    JSIOCGAXMAP = load_JSIOCGAXMAP()
    MAX_NR_AXES = load_MAX_NR_AXES()
    container = array.array('B', [0] * MAX_NR_AXES)
    fcntl.ioctl(joystick, JSIOCGAXMAP, container)  

    nr_axes = load_nr_axes(joystick)
    axes = list(container[:nr_axes])

    return axes_event_codes


def load_buttons_event_codes(joystick):
    """Load button input event codes"""
    JSIOCGBTNMAP = load_JSIOCGBTNMAP()
    MAX_NR_BUTTONS = load_MAX_NR_BUTTONS()
    container = array.array('H', [0] * MAX_NR_BUTTONS)
    fcntl.ioctl(joystick, JSIOCGBTNMAP, container)

    nr_buttons = load_nr_buttons(joystick)
    # BTN_MISC = load_BTN_MISC()
    # buttons = [btn - BTN_MISC for btn in container[:nr_buttons]]
    buttons = list(container[:nr_buttons])

    return buttons
