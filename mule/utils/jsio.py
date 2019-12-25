import logging
# TODO: log import errors
logging.debug("jsio module".format())

try:

    logging.debug("Attempting to load utilities._jsio methods.".format())
    #logging.debug("Note: PURPOSELY skipping this for now!".format())
    #raise ImportError
    #logging.debug("Importing utilities._jsio".format())
    #raise ImportError

    from utilities._jsio import (retrieve_JSIOCGAXES,
                                 retrieve_JSIOCGBUTTONS,
                                 retrieve_JSIOCGNAME,
                                 retrieve_JSIOCGAXMAP,
                                 retrieve_JSIOCGBTNMAP,
                                 retrieve_MAX_NR_AXES,
                                 retrieve_MAX_NR_BUTTONS,
                                 retrieve_JS_EVENT_AXIS,
                                 retrieve_JS_EVENT_BUTTON,
                                 retrieve_JS_EVENT_INIT)
    
except ImportError:
    logging.debug("utilities._jsio import FAILED".format())
    logging.debug("Hard-coding events".format())
    
    # These constants can be retrieved manually by parsing and evaluating
    # code from the following header files in the raspbian linux source:
    # asm-generic/ioctl.h
    # asm-generic/ll64.h
    # linux/input-event-codes.h
    # linux/joystick.h
    logging.debug("_jsio FAILED. Hard coded events used.".format())
        
    def retrieve_JS_EVENT_BUTTON():
        return 0x01

    def retrieve_JS_EVENT_AXIS():
        return 0x02

    def retrieve_JS_EVENT_INIT():
        return 0x80

    def retrieve_JSIOCGAXES():
        return 0x80016a11

    def retrieve_JSIOCGBUTTONS():
        return 0x80016a12

    def retrieve_JSIOCGNAME(name_length):
        SIZESHIFT = 16
        return 0x80006a13 + (name_length << SIZESHIFT)

    def retrieve_JSIOCGAXMAP():
        return 0x80406a32

    def retrieve_JSIOCGBTNMAP():
        return 0x84006a34

    def retrieve_MAX_NR_AXES():
        return 0x40

    def retrieve_MAX_NR_BUTTONS():
        return 0x200


