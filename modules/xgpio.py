#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import time
import RPi.GPIO as GPIO
from .xutils import xmsg
from threading import Thread

#base class for managing GPIO process
class XGPIO(object):
    def __init__(self, pins, sra=True): #sra=start signal thread right away
        self.gpio = GPIO
        self.pins = pins
        self.send_signal_thread = None
        self.current_state = GPIO.HIGH
        self.setup()
        if sra: self.start_thread(pins=[12])
    
    def setup(self):
        self.gpio.setmode(GPIO.BCM)
        self.gpio.setup(self.pins, GPIO.OUT)

    def release(self):
        self.gpio.cleanup()
    
    def send_thread(self, pins):
        assert len(pins) != 0, 'incorrect pins number list.'
        
        while True:
            self.gpio.output(pins, self.current_state)
            time.sleep(0.1)
    
    def start_thread(self, pins):
        self.send_signal_thread = Thread(target=self.send_thread, args=(pins,), group=None)
        self.send_signal_thread.start()