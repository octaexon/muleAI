import iterator
import logging

from .base import BasePart, ThreadComponent


class ToggleTransformer:
    def __init__(self, button_ref, state_key, toggle_modes):
        self.button_ref = button_ref
        self.state_key = state_key
        self.toggle = iterator.cycle(state_modes)

    def transform(self, state, value):
        state[self.state_key] = next(self.toggle)

class SlideTransformer:
    def __init__(self, inc_ref, dec_ref, state_key):


class AxisTransformer:
    def __init__(self, axis_ref, state_key):
        self.axis_ref = axis_ref
        self.state_key = state_key

    def transform(self, state, value):
        state[self.state_key] = value




class ModeController(DigitalController):
    def __init__(self, steering='human', throttle='human', recording=False):
        self.steering = steering
        self.throttle = throttle
        self.recording = recording



# TODO: set up auto-recording
# TODO: delay (reduced user mobility)
# TODO: publish modes to state as a list/dict with one turned on?? 
#       I don't see the reason right now, but it was a thought
# TODO: Controllers should only produce the raw signal, there should be a
#       separate part to do the manipulation, flipping, scaling, adapting to actuators, etc.

class PS3Controller(BasePart):
    input_keys = ()
    output_keys = ('steering_signal', 'throttle_signal', 'mode')

    def __init__(self, device_path='/dev/input/js0', 
                       steering='human', 
                       throttle='human', 
                       recording=False,
                       flip_steering=False, 
                       flip_throttle=False):

        self.joystick = JoystickDevice(device_path)
        self.mode = {'steering': 'human', 'throttle': 'human', 'recording': False}

        self.steering_signal = 0.0
        self.throttle_signal = 0.0

        self.steering_scale = 1.0;
        self.throttle_scale = 1.0;

        self.steering_flip = -1.0 if flip_steering else 1.0
        self.throttle_flip = -1.0 if flip_throttle else 1.0

        self.thread = ThreadComponent(self._update)

    def start(self):
        self.joystick.open()
        self.thread.start()


    def transform(self, state):
        state['steering_signal'] = self.steering_signal
        state['throttle_signal'] = self.throttle_signal
        state['mode'] = self.mode


    def stop(self):
        self.thread.stop()
        self.joystick.close()


    def _update(self):
        ''' Update steering and throttle signals
        * axis-thumb-left-x     | steering
        * axis-thumb-right-y    | throttle
        * button-dpad-up        | increase throttle scale
        * button-dpad-down      | decrease throttle scale
        * button-dpad-left      | increase steering scale 
        * button-dpad-right     | decrease steering scale
        * button-triangle       | toggle mode
        * button-circle         | toggle recording
        '''
        THROTTLE_SCALE_SHIFT = 0.05
        STEERING_SCALE_SHIFT = 0.05

        tag, value = self.joystick.poll()
        print(tag, value)
        if tag == 'axis-thumb-left-x':
            # actuators expect:
            # +ve signal indicates left
            # -ve signal indicated right
            # however, from the joystick interface:
            # +ve value indicates thumb was moved right
            # -ve value indicates thumb was moved left
            # hence the presence of (-value)
            # to allow for an on the fly fudge factor, steering_flip can be activated
            self.steering_signal = self.steering_scale * self.steering_flip * (-value)

        elif tag == 'axis-thumb-right-y':
            # actuators expect:
            # +ve signal indicates forward
            # -ve signal indicates reverse
            # however, from the joystick interface:
            # +ve value indicate the thumb was pulled back
            # -ve value indicates thumb was pushed forward
            # hence the presence of (-value)
            # to allow for an on the fly fudge factor, throttle_flip can be activated
            self.throttle_signal =  self.throttle_scale * self.throttle_flip * (-value)

        elif tag == 'button-dpad-up' and value == 1:
            self.throttle_scale = min(1.0, self.throttle_scale + THROTTLE_SCALE_SHIFT)

        elif tag == 'button-dpad-down' and value == 1:
            self.throttle_scale = max(0.0, self.throttle_scale - THROTTLE_SCALE_SHIFT)

        elif tag == 'button-dpad-right' and value == 1:
            self.steering_scale = min(1.0, self.steering_scale + STEERING_SCALE_SHIFT)

        elif tag == 'button-dpad-left' and value == 1:
            self.steering_scale = max(0.0, self.steering_scale - STEERING_SCALE_SHIFT)

        elif tag == 'button-triangle' and value == 1:
            self.mode['steering'] = 'human'
            self.mode['throttle'] = 'human'

        elif tag == 'button-square' and value == 1:
            self.mode['steering'] = 'human'
            self.mode['throttle'] = 'ai'

        elif tag == 'button-circle' and value == 1:
            self.mode['steering'] = 'ai'
            self.mode['throttle'] = 'human'

        elif tag == 'button-cross' and value == 1:
            self.mode['steering'] = 'ai'
            self.mode['throttle'] = 'ai'

        elif tag == 'button-select' and value == 1:
            self.mode['recording'] = not self.mode['recording']
