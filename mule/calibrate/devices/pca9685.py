import logging.config
import os

import yaml

from mule import CAL_DAT

logger = logging.getLogger(__name__)

# PCA9685 default parameters
REF = 'pwm'
CLASS = 'PCA9685'
ADDRESS = '0x40'
FREQUENCY = 50


def calibrate():
    """Calibration of PCA9685 board.

       1. Create a reference for the calibrated device.

       2. The default (or base) address for the Adafruit PCA9685 board is 0x40.
       However, this address can incremented by soldering some contacts 
       (which would need to be done if the boards were to be chained). In any
       case, the address can be checked once connected to the i2c interface 
       of Raspberry Pi using:

           sudo i2cdetect -y 1

       where 1 signifies the default i2cbus on the Raspberry Pi.

       3. The board allows for a refresh rate between 24Hz and 1526Hz. The 
       default here is 50Hz for two reasons:
        - typical servo motors expect a refresh rate in the neighbourhood of
          50Hz
        - typical esc modules expect 30Hz to 60Hz

       Since the refresh rate is board-wide, to add channels at different
       frequencies, one would need to chain another board.
    """

    print(calibrate.__doc__)

    logger.info('Calibrating PCA9685')

    ref = input(f'Enter reference (default: {REF}): ') or REF
    # klass = input(f'Enter class (default: {CLASS}): ') or CLASS
    address = input(f'Enter address (default: {ADDRESS}): ') or ADDRESS
    address = int(address, base=16)

    frequency = input(f'Enter frequency (default: {FREQUENCY}): ') or FREQUENCY
    frequency = int(frequency)

    logger.info(f'PCA9685 calibrated')
    logger.info(f'Reference: {ref}')
    logger.info(f'Class:     {CLASS}')
    logger.info(f'Address:   0x{address:X}')
    logger.info(f'Frequency: {frequency}')

    # construct parameters dictionary
    params = {}
    params['ref'] = ref
    params['class'] = CLASS
    params['args'] = {'address': address, 'frequency': frequency}

    path = os.path.join(CAL_DAT, ref + '.yml')

    with open(path, 'w') as f:
        yaml.dump(params, f)

    logger.info(f'Calibration data saved to: {path}')
