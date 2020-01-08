"""Joystick device calibration."""

import logging
import os
import struct

import yaml

from ..ext import jsio
from mule import CAL_DAT, CAL_JOY

logger = logging.getLogger(__name__)

REF = 'js'
CLASS = 'JoystickDevice'
DEVICE_DIR = '/dev/input'  # default directory for input interfaces on RPi


def calibrate():
    """Calibration of joystick device.

    1. Create a reference for the device.

    2. Enter the directory where joystick devices are mounted.  From there, 
    devices are listed.  Choose the appropriate device.

    3. Enter the index associated with the appropriate keymap.

    4. Event types are loaded, removes the need for inclusion of jsio library in
    drive code.

    """
    ref = input(f'Create a keymap reference (default: {REF}): ') or REF

    device_dir = input(
        f'Enter input device directory (default: {DEVICE_DIR}): ') or DEVICE_DIR

    device_paths = [
        os.path.join(device_dir, dp) for dp in os.listdir(device_dir)
        if not dp.startswith('.')
    ]

    for i, dp in enumerate(device_paths):
        print(f'{i}: {dp}')

    idx = input(f'Enter index associated to device path: ')
    idx = int(idx)

    device_path = device_paths[idx]

    keymap_paths = [
        os.path.join(CAL_JOY, kp) for kp in os.listdir(CAL_JOY)
        if not kp.startswith('.')
    ]

    for i, kp in enumerate(keymap_paths):
        print(f'{i}: {kp}')

    idx = input(f'Enter index associated to appropriate keymap path: ')
    idx = int(idx)

    keymap_path = keymap_paths[idx]

    with open(keymap_path, 'r') as f:
        keymap = yaml.full_load(f)

    event_types = jsio.load_event_types()

    # Create parameter dictionary
    params = {}
    params['ref'] = ref
    params['class'] = CLASS

    args = {}
    args['device_path'] = device_path
    args['keymap_path'] = keymap_path
    params['event_types'] = event_types
    params['axes'] = keymap['axes']
    params['buttons'] = keymap['buttons']

    path = os.path.join(CAL_DAT, ref + '.yml')

    with open(path, 'w') as f:
        yaml.dump(params, f)

    logger.info(f'Calibration data saved to: {path}')
