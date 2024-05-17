#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import time
from .xutils import xmsg
from threading import Thread

try:
    import RPi.GPIO as GPIO
except:
    #for development on Windows
    class GPIO(object):
        def __init__(self):
            self.LOW = 0
            self.HIGH = 1
            self.BCM = 2
            self.OUT = 3
        def setmode(self, mode): pass
        def setup(self, pins, state): pass
        def output(self, pins, state): pass
        def cleanup(self): pass

#base class for managing GPIO process
class XGPIO(object):
    def __init__(self, pins, sra=True): #sra=start signal thread right away
        self.gpio = GPIO()
        self.pins = pins
        self.running = False
        self.send_signal_thread = None
        self.current_state = self.gpio.HIGH
        self.setup()
        if sra: self.start_thread(pins=[12])
    
    def setup(self):
        xmsg('GPIO connection was established.')
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.pins, self.gpio.OUT)

    def release(self):
        self.running = False
        self.gpio.cleanup()
        xmsg('GPIO connection was released.')
    
    def send_thread(self, pins):
        assert len(pins) != 0, 'incorrect pins number list.'
        #repeatedly send signal to the tower
        while True:
            if self.running:
                self.gpio.output(pins, self.current_state)
                time.sleep(0.1)
            else:
                break
    
    def start_thread(self, pins):
        self.send_signal_thread = Thread(target=self.send_thread, args=(pins,), group=None)
        self.running = True
        self.send_signal_thread.start()
        xmsg('GPIO sending signal thread was started.')