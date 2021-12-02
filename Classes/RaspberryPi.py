import RPi.GPIO as io
import logging

class RaspberryPi():
    # IN1 - IN4
    pin6 = 6
    pin13 = 13
    pin19 = 19
    pin26 = 26

    

    def __init__(self):
        self.logger = logging.getLogger('MarsRover.RaspberryPi')
        self.logger.debug(f'init {RaspberryPi.__name__}')

        self.setGpioMode(io.BCM)
        self.setGpioWarnings(False)

        io.setup(self.pin6, io.OUT)
        io.setup(self.pin13, io.OUT)
        io.setup(self.pin19, io.OUT)
        io.setup(self.pin26, io.OUT)

        io.output(self.pin6, io.LOW)
        io.output(self.pin13, io.LOW)
        io.output(self.pin19, io.LOW)
        io.output(self.pin26, io.LOW)

    def gpioCleanup(self):
        self.logger.debug(f"clean gpio pins")
        io.output(6, False)
        io.output(13, False)
        io.output(19, False)
        io.output(26, False) 
        io.cleanup()
        self.logger.debug('clean complete')

    def setGpioMode(self, mode):
        self.logger.debug(f'set gpio mode to {mode}')
        io.setmode(mode)

    def setGpioWarnings(self, receiveWarnings):
        self.logger.debug(f'set gpio warnings to {receiveWarnings}')
        io.setwarnings(receiveWarnings)
