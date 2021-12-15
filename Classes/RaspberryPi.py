import RPi.GPIO as RPiIO
import logging

class RaspberryPi():
    pin6 = 6
    pin13 = 13
    pin19 = 19
    pin26 = 26
    pin23 = 23
    pin25 = 25

    IN = RPiIO.IN # 1
    OUT = RPiIO.OUT # 0
    LOW = RPiIO.LOW # 0
    HIGH = RPiIO.HIGH # 1
    
    def __init__(self):
        self.logger = logging.getLogger("MarsRover.RaspberryPi")

        self.setGpioMode(RPiIO.BCM)
        self.setGpioWarnings(False)

        # MotorController IN1 - IN4
        self.setup(self.pin6, self.OUT)
        self.setup(self.pin13, self.OUT)
        self.setup(self.pin19, self.OUT)
        self.setup(self.pin26, self.OUT)
        self.setOutput(self.pin6, self.LOW)
        self.setOutput(self.pin13, self.LOW)
        self.setOutput(self.pin19, self.LOW)
        self.setOutput(self.pin26, self.LOW)

        # Environment Hat LUX
        # self.setup(self.pin23, self.OUT)
        # print("start")
        # self.setOutput(self.pin23, self.LOW)
        # print("end")
    
    def gpioCleanup(self):
        self.setOutput(self.pin6, self.LOW)
        self.setOutput(self.pin13, self.LOW)
        self.setOutput(self.pin19, self.LOW)
        self.setOutput(self.pin26, self.LOW)
        RPiIO.cleanup()

    def setGpioMode(self, mode):
        self.logger.debug(f'set gpio mode to {mode}')
        RPiIO.setmode(mode)

    def setGpioWarnings(self, receiveWarnings):
        self.logger.debug(f'set gpio warnings to {receiveWarnings}')
        RPiIO.setwarnings(receiveWarnings)

    def setOutput(self, pin, output):
        RPiIO.output(pin, output)

    def setup(self, pin, value):
        RPiIO.setup(pin, value)

