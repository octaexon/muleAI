from . import pca9685
from . import joystick_keymap
from . import joystick_device
from . import pwm_channel


registry = {}
registry['pca9685'] = pca9685.calibrate
registry['joystick_keymap'] = joystick_keymap.calibrate
registry['joystick_device'] = joystick_device.calibrate
registry['pwm_channel'] = pwm_channel.calibrate 
registry['servo'] = pwm_channel.calibrate 
registry['esc'] = pwm_channel.calibrate 
