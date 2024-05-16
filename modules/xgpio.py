#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import RPi.GPIO as GPIO

class XGPIO(object):
    def __init__(self, pins):
        self.gpio = GPIO
        self.pins = pins
        self.release()
        self.setup()
    
    def setup(self):
        self.gpio.setmode(GPIO.BCM)
        self.gpio.setup(self.pins, GPIO.OUT)

    def release(self):
        self.gpio.cleanup()
    
    def send(self, pins, state):
        assert len(pins) != 0, 'incorrect pins number list.'
        self.gpio.output(pins, state)