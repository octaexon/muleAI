"""PWM channel calibration."""

import logging

from mule import CAL_DAT 
import mule.drive.devices as devices

logger = logging.getLogger(__name__)

CLASS = 'PWMChannel'

def _calibrate_pulse_width(controller, channel):
    width = controller.DEFAULT_WIDTH
    while True:
        ref = input(f'Create pulse reference: ')
        if not _ref:
            break
        _width = input(
            f'Enter pulse width (s) (currently: {width}): '
        )
        if not _width:
            break
        width = float(_width)
        controller.set_pulse_width(channel, width)

    # reset to default pulse width
    controller.set_pulse_width(channel, controller.DEFAULT_WIDTH)

    return width, ref


def calibrate():
    """Calibration of PWM channels associated to a PWM device.

    The aim is to calibrate a sequence of pulse wave widths.

    For example, the typical servo motor expects a 1-2ms pulse width per cycle 
    and is robust to changes in the cycle period, that is, the refresh rate. 
    However, the specific usage of the servo may dictate a restricted angle of
    rotation, for example, to control the steering angle of a vehicle.
    Therefore, it is worthwhile calibrating the full left, straight and full
    right pulse widths.

    1. Create a reference for the channel.

    2. Enter the PWM device reference to which the channel is associated.

    3. Enter channel identifier on the PWM device.

    4. Calibrate sequence of pulse widths.

    Note:

    The pulse 
    """

    print(calibrate.__doc__)

    logging.info('Calibrating PWM Channel')

    ref = input('Create pwm channel reference: ')
    pwm_ref = input(f'Enter PWM device reference: ')

    # load calibration data for pwm device and create device
    pwm_path = os.path.join(CAL_DAT, pwm_ref + '.yml')
    with open(pwm_path, 'r') as f:
        pwm_params = yaml.full_load(f)
        pwm_class = pwm_params['class']
        pwm_args = pwm_params['args']
        pwm = devices.registry[pwm_class](**pwm_args)

    channel = input('Enter channel on PWM controller: ')
    channel = int(channel)

    pulses = {}
    while True: 
        width, ref = _calibrate_pulse_width(controller, channel)
        if not ref:
            break
        pulses[ref] = width


    logger.info('PWM channel calibrated')
    logger.info('Reference: {ref}')
    logger.info('Class:     {CLASS}')
    logger.info('PWM device reference: {pwm_ref}')
    logger.info('PWM device channel: {channel}')
    for k, v in pulses.items():
        logger.info('Pulse: {k}, width (s): {v}')

    # Construct parameter dictionary
    params = {}
    params['ref'] = ref
    params['class'] = CLASS

    args = {}
    args['pwm_ref'] = pwm_ref
    args['channel'] = channel
    args['pulses'] = pulses
    params['args'] = args

    path = os.path.join(CAL_DAT, ref + '.yml')
    with open(path, 'w') as f:
        yaml.dump(params, f)

    logger.info(f'Calibration data saved to: {path}')
