from .base import BasePart
import random
import logging
import time
import RPi.GPIO as GPIO

class setup_GPIO(BasePart):
    """This part should be before any other LED parts in the configuration!
    
    
    """
    input_keys = ()
    output_keys = ()
    def __init__(self):
        pass

    def start(self):
        """ """
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        
    def transform(self, state):
        pass

    def stop(self):
        pass


class record_LED(BasePart):
    input_keys = ('mode',)
    output_keys = ()
    def __init__(self,PIN_RED):
        self.PIN_RED = PIN_RED

    def start(self):
        """ """
        #GPIO.setwarnings(False)
        #GPIO.cleanup()
        #GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_RED,GPIO.OUT)
        GPIO.output(self.PIN_RED,  False)
        
    def transform(self, state):
        if state['mode']['recording'] == True:
            GPIO.output(self.PIN_RED,  True)
        elif state['mode']['recording'] == False:         
            GPIO.output(self.PIN_RED,  False)

    def stop(self):
        GPIO.output(self.PIN_RED,  False)

        
class sequential_LED_loop(BasePart):
    """ """
    input_keys = ()
    output_keys = ('led_flags',)
    
    def __init__(self,PIN_BLUE1,PIN_BLUE2,PIN_BLUE3, PIN_BLUE4  ):
        self.NUMBER_LED = 4
        self.lights_off = [False for i in range(self.NUMBER_LED)]
        self.lights_on = [True for i in range(self.NUMBER_LED)]
        
        self.PIN_BLUE1   = PIN_BLUE1
        self.PIN_BLUE2   = PIN_BLUE2
        self.PIN_BLUE3   = PIN_BLUE3 
        self.PIN_BLUE4   = PIN_BLUE4
        
        self.count = 0
        
    def start(self):
        """ """
        #state['led_flags'] = self.lights_on
        #GPIO.setwarnings(False)
        #GPIO.cleanup()
        #GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.PIN_BLUE1,GPIO.OUT)
        GPIO.setup(self.PIN_BLUE2,GPIO.OUT)
        GPIO.setup(self.PIN_BLUE3,GPIO.OUT)
        GPIO.setup(self.PIN_BLUE4,GPIO.OUT)

    def transform(self, state):
        """ """
        #state['led_flags'] = self.lights_off
        
        #TODO: Why is self.lights_off being changed???
        state['led_flags'] = [False for i in range(self.NUMBER_LED)]
        #print("Falses:", self.lights_off)
        #print("Before: ",state['led_flags'])
 
        if self.count%5 != 0:
            #print("Turn on this LED:",self.count%5-1)
            state['led_flags'][self.count%5-1] = True
            
        #print("After:",state['led_flags'])
        self.count += 1
        
        GPIO.output(self.PIN_BLUE1,  state['led_flags'][0])
        GPIO.output(self.PIN_BLUE2,  state['led_flags'][1])
        GPIO.output(self.PIN_BLUE3,  state['led_flags'][2])
        GPIO.output(self.PIN_BLUE4,  state['led_flags'][3])

    def stop(self):
        '''  '''
        GPIO.output(self.PIN_BLUE1,  self.lights_off[0])
        GPIO.output(self.PIN_BLUE2,  self.lights_off[1])
        GPIO.output(self.PIN_BLUE3,  self.lights_off[2])
        GPIO.output(self.PIN_BLUE4,  self.lights_off[3])
    
class random_onoff_LED_loop(BasePart):
    
    ''' asdf '''
    input_keys = ()
    output_keys = ('led_flags',)
    #output_keys = ()

    def __init__(self,PIN_BLUE1,PIN_BLUE2,PIN_BLUE3, PIN_BLUE4  ):
        raise "OBSELETE"
        NUMBER_LED = 4
        self.lights_off = [False for i in range(NUMBER_LED)]
        self.lights_on = [True for i in range(NUMBER_LED)]
        
        self.PIN_BLUE1   = PIN_BLUE1
        self.PIN_BLUE2   = PIN_BLUE2
        self.PIN_BLUE3   = PIN_BLUE3 
        self.PIN_BLUE4   = PIN_BLUE4
        
    def start(self):
        ''' asdf '''
        #state['led_flags'] = self.lights_on
        GPIO.setwarnings(False)
        
        GPIO.cleanup()
        
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.PIN_BLUE1,GPIO.OUT)
        GPIO.setup(self.PIN_BLUE2,GPIO.OUT)
        GPIO.setup(self.PIN_BLUE3,GPIO.OUT)
        GPIO.setup(self.PIN_BLUE4,GPIO.OUT)
        
    def transform(self, state):
        ''' asdf
        '''
        last_flags = state['led_flags']
        
        coin_flips = [random.random() < 0.5 for i in range(5)]
        #print(coin_flips)
        state['led_flags'] = coin_flips
        
        GPIO.output(PIN_BLUE1,  state['led_flags'][0])
        GPIO.output(PIN_BLUE2,  state['led_flags'][1])
        GPIO.output(PIN_BLUE3,  state['led_flags'][2])
        GPIO.output(PIN_BLUE4,  state['led_flags'][3])
        
        #print(bool(random.getrandbits(5)))
        #print(random.sample([True, False],5))
        #if coin_flip: state['led_flags'] = self.lights_on
        #else:  state['led_flags'] = self.lights_off

    def stop(self):
        '''  '''
        GPIO.output(PIN_BLUE1,  self.lights_off[0])
        GPIO.output(PIN_BLUE2,  self.lights_off[1])
        GPIO.output(PIN_BLUE3,  self.lights_off[2])
        GPIO.output(PIN_BLUE4,  self.lights_off[3])
        
