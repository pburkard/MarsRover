import RPi.GPIO as GPIO_
import logging
from marsrovercore.enums import Pin, PinSignalDirection, PinSignalState

class GPIO():
    def __init__(self):
        self.logger = logging.getLogger("MarsRover.RaspberryPi")

        self.set_mode(GPIO_.BCM)
        self.set_warnings(True)

        # Motor Controller 1
        self.init_output(Pin.MC1_IN1)
        self.init_output(Pin.MC1_IN2)
        self.init_output(Pin.MC1_IN3)
        self.init_output(Pin.MC1_IN4)
        
        # Motor Controller 2
        self.init_output(Pin.MC2_IN1)
        self.init_output(Pin.MC2_IN2)
        self.init_output(Pin.MC2_IN3)
        self.init_output(Pin.MC2_IN4)

        # Environment hat light sensor
        # self.init_input(Pin.ENVH_LIGHT)

        # Distance sensor
        self.init_output(Pin.DISTANCE_XSHUT, signal_state=PinSignalState.HIGH)
    
    def cleanup_all(self):
        self.logger.debug("cleanup all")
        GPIO_.cleanup()

    def cleanup(self, pins:list):
        self.logger.debug(f'cleanup: {pins}')
        GPIO_.cleanup(pins)

    def set_mode(self, mode):
        self.logger.debug(f'set gpio mode to {mode}')
        GPIO_.setmode(mode)

    def set_warnings(self, receiveWarnings:bool):
        GPIO_.setwarnings(receiveWarnings)

    def init_output(self, pin:Pin, signal_state:PinSignalState=PinSignalState.LOW):
        self.logger.debug(f"init output {repr(pin)}, {repr(signal_state)}")
        GPIO_.setup(pin.value, PinSignalDirection.OUTPUT.value, initial=signal_state.value)

    def init_input(self, pin:Pin):
        self.logger.debug(f"init input {repr(pin)}")
        GPIO_.setup(pin.value, PinSignalDirection.INPUT.value)
    
    def set_signal_state(self, pin:Pin, signal_state:PinSignalState):
        self.logger.debug(f"set {repr(pin)} to {repr(signal_state)}")
        GPIO_.output(pin.value, signal_state.value)

