"""Joystick keymap calibration."""

import logging
import os
import struct

import yaml

from ..ext import jsio
from mule import CAL_JOY

logger = logging.getLogger(__name__)

DEVICE_DIR = '/dev/input'  # default directory for input interfaces on RPi


def calibrate():
    """Calibration of joystick keymap.

    1. Create a reference for the keymap.

    2. Enter the directory where joystick devices are mounted.  From there, 
    devices are listed.  Choose the appropriate device.

    3. The device is then opened and each detected axis and button is run
    through in sequence and is given a (hopefully) descriptive reference, for
    example, 'dpad-left', 'circle', 'right-stick-x'.
    """

    ref = input(f'Create a keymap reference: ')

    device_dir = input(
        f'Enter input device directory (default: {DEVICE_DIR}): '
    ) or DEVICE_DIR

    device_paths = [
        os.path.join(device_dir, dp) for dp in os.listdir(device_dir)
        if not dp.startswith('.')
    ]

    for i, dp in enumerate(device_paths):
        print(f'{i}: {dp}')

    idx = input(f'Enter index associated to device path: ')
    idx = int(idx)

    device_path = device_paths[idx]

    logger.debug(f'Opening {device_path}.')

    with open(device_path, 'rb') as joystick:
        event_types = jsio.load_event_types()
        nr_axes = jsio.load_nr_axes(joystick)
        nr_buttons = jsio.load_nr_buttons(joystick)

        axes = [''] * nr_axes
        buttons = [''] * nr_buttons

        for i in range(nr_axes):
            print(f'Identify axis {i+1} of {nr_axes} (press crtl-C to exit):')
            try:
                while True:
                    event = joystick.read(8)
                    if event:
                        timestamp, event_value, event_type, event_key = struct.unpack(
                            'IhBB', event)

                        if (event_type
                                & event_types['axis']) and (event_key == i):
                            print(f'Axis {i+1:>3} | Value: {event_value:>6}',
                                  end='\r')

                        else:
                            pass

            except KeyboardInterrupt:
                axes[i] = input(
                    f'\nCreate reference (leave blank to ignore): ')

        for i in range(nr_buttons):
            print(
                f'Identify button {i+1} of {nr_buttons} (press crtl-C to exit):'
            )
            try:
                while True:
                    event = joystick.read(8)
                    if event:
                        timestamp, event_value, event_type, event_key = struct.unpack(
                            'IhBB', event)

                        if (event_type
                                & event_types['button']) and (event_key == i):
                            print(f'Button {i+1:>3} | Value: {event_value:>2}',
                                  end='\r')

                        else:
                            pass

            except KeyboardInterrupt:
                buttons[i] = input(
                    f'\nCreate reference (leave blank to ignore): ')

    axes = {i: axis for i, axis in enumerate(axes) if axis}
    buttons = {i: button for i, button in enumerate(buttons) if button}

    # Create parameter dictionary
    params = {}
    params['ref'] = ref
    params['axes'] = axes
    params['buttons'] = buttons

    path = os.path.join(CAL_JOY, ref + '.yml')

    with open(path, 'w') as f:
        yaml.dump(params, f)

    logger.info(f'Calibration data saved to: {path}')
