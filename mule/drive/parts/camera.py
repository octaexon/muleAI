import time
import logging

import numpy as np
import cv2 as cv2

from .base import BasePart, ThreadComponent

class BaseCam(BasePart):
    ''' Functionality and state common to all cameras

        The main task of this base class is to incorporate threading
        capabilities for each camera object

        class-level members:

        input_keys, output_keys: tuples
        keys to access vehicle state dictionary

        Child classes should update RGB images
    '''
    input_keys = ()
    output_keys = ('camera_array',)


    def __init__(self, resolution, framerate, threaded=False):
        self.resolution = resolution
        self.framerate = framerate
        self.threaded = threaded

        self.frame = None

        if self.threaded:
            self.thread = ThreadComponent(self._update)


    def start(self):
        ''' Start thread if requested '''
        if self.threaded:
            self.thread.start()


    def transform(self, state):
        ''' Transform vehicle state using _update, which is re-implemented
            in child classes

            Arguments

            state: dict
            stores elements comprising vehicle state, for example,
            latest image received from camera
        '''
        if not self.threaded:
            self._update()

        state['camera_array'] = self.frame
        #logging.debug("Camera shape: {}, max_value: {}".format(state['camera_array'].shape, np.max(state['camera_array'])))




    def stop(self):
        ''' Stop thread if started '''
        if self.threaded:
            self.thread.stop()


    def _update(self, **kwargs):
        ''' Updates part state '''
        pass
    

# TODO: impore framerate using Regulator class
# TODO: allow for changing color inn stream of images
class MockCam(BaseCam):
    ''' Mock camera spewing out black images

        Useful for testing drive loop without the need for a functioning
        camera
    '''
    def __init__(self, resolution=(160, 120), framerate = 24, threaded=True):
        super().__init__(resolution, framerate, threaded)

    def start(self):
        ''' Start "camera" with constant black image '''
        self.camera = np.zeros(shape=(self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
        super().start()

    def stop(self):
        super().stop()

    def _update(self):
        self.frame = np.array(self.camera)


# TODO: MJ - Add the members to __init__
class PiCam(BaseCam):
    ''' Raspberry Pi camera '''
    def __init__(self, resolution=(160, 120), framerate=24, threaded=False, colormode='YUV'):

        self.colormode = colormode

        logging.debug("PiCam set to {} mode".format(self.colormode))

        super().__init__(resolution, framerate, threaded)


    def start(self):
        ''' Starts camera and captures repeatedly at the chosen framerate 

            https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera.PiCamera.capture_continuous
        '''
        import picamera
        self.camera = picamera.PiCamera(resolution=self.resolution, framerate=self.framerate)

        # warm-up
        time.sleep(1)

        import picamera.array
        # second argument engages the GPU resizer to ensure the desired resolution
        # as the camera may capture only at certain resolutions predetermined resolutions
        # the capture stream is an iterator that updates self.frame each time it is iterated
        #mode = 'RGB'
        if self.colormode=='RGB':
            self.rgb_or_yuv_stream = picamera.array.PiRGBArray(self.camera, self.resolution)
            #self.array_stream = self.rgb_stream
            self.stream = self.camera.capture_continuous(self.rgb_or_yuv_stream, format='rgb', use_video_port=True)
        elif self.colormode=='YUV':
            self.rgb_or_yuv_stream = picamera.array.PiYUVArray(self.camera, self.resolution)
            #self.this_stream = self.yuv_stream
            self.stream = self.camera.capture_continuous(self.rgb_or_yuv_stream, format='yuv', use_video_port=True)
        else:
            raise

        super().start()


    def stop(self):
        super().stop()

        self.stream.close()
        self.rgb_or_yuv_stream.close()
        self.camera.close()


    def _update(self):
        self.frame = next(self.stream).array
        self.rgb_or_yuv_stream.seek(0)

    @property
    def _class_string(self):
        return "{} {}".format(self.__class__.__name__, self.resolution)


# TODO: impose framerate
# TODO: add device search -- on the pi, there is the possibility for multiple devices
#                            but for one webcam, it will be 0 (I think).
#                            if not, then >> ls -l /dev/video*

class WebCam(BaseCam):
    ''' Web camera 

        Most web cameras are not so flexible as to allow for arbitrary
        resolution, for example, the macbook air iSight camera allows
        for a small subset of resolutions between (1280x720) and (320x240)
        See self._crop

        Note: if asked for a higher resolution than supported by the hardware, 
        it does not perform a crop (in that dimension)
    '''
    def __init__(self, resolution=(160, 120), framerate=24, threaded=False):
        super().__init__(resolution, framerate, threaded)

    def start(self):
        ''' Start camera and set resolution 
        '''
        # 0 is default web camera device number
        self.camera = cv2.VideoCapture(0)
        # with limited success
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        # warm up
        time.sleep(1)

        super().start()

    def stop(self):
        super().stop()

        self.camera.release()

    def _update(self):
        ''' Update self.frame

            Note: opencv deals in BGR rather than RGB images by default
        '''
        self.frame = self._crop(cv2.cvtColor(self.camera.read()[1], cv2.COLOR_BGR2RGB))

    def _crop(self, image):
        ''' Ensures that images are cropped to the requested resolution '''
        padding_height = max((image.shape[0] - self.resolution[1]) // 2, 0)
        padding_width = max((image.shape[1] - self.resolution[0]) // 2, 0)

        return image[padding_height:image.shape[0]-padding_height, 
                     padding_width:image.shape[1]-padding_width]

    @property
    def _class_string(self):
        return "{} {} at {} frames per second".format(self.__class__.__name__, self.resolution, self.framerate)
