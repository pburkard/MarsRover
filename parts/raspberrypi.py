import RPi.GPIO as RPiIO
import logging
from enum import Enum

class RaspberryPi():
    BUS0_SDA=2
    BUS0_SCL=3
    BUS3_SDA=23
    BUS3_SCL=24
    EH_LUX=10
    TOF_XSHUT=25
    MC1_IN1=6
    MC1_IN2=13
    MC1_IN3=19
    MC1_IN4=26
    MC2_IN1=12
    MC2_IN2=16
    MC2_IN3=20
    MC2_IN4=21

    IN = RPiIO.IN # 1
    OUT = RPiIO.OUT # 0
    LOW = RPiIO.LOW # 0
    HIGH = RPiIO.HIGH # 1
    
    def __init__(self):
        self.logger = logging.getLogger("MarsRover.RaspberryPi")

        self.setGPIOMode(RPiIO.BCM)
        self.setGPIOWarnings(True)

        # Motor Controller 1
        self.setGPIO(self.MC1_IN1, self.OUT, self.LOW)
        self.setGPIO(self.MC1_IN2, self.OUT, self.LOW)
        self.setGPIO(self.MC1_IN3, self.OUT, self.LOW)
        self.setGPIO(self.MC1_IN4, self.OUT, self.LOW)
        
        # Motor Controller 2
        self.setGPIO(self.MC2_IN1, self.OUT, self.LOW)
        self.setGPIO(self.MC2_IN2, self.OUT, self.LOW)
        self.setGPIO(self.MC2_IN3, self.OUT, self.LOW)
        self.setGPIO(self.MC2_IN4, self.OUT, self.LOW)

        # Environment Hat LUX
        # self.setup(self.EH_LUX, self.OUT)
        # self.setOutput(self.EH_LUX, self.LOW)
    
    def cleanupAllGPIOs(self):
        RPiIO.cleanup()

    def cleanupGPIOs(self, channels: list):
        self.logger.debug(f'cleanup GPIOs: {channels}')
        RPiIO.cleanup(channels)

    def setGPIOMode(self, mode):
        self.logger.debug(f'set gpio mode to {mode}')
        RPiIO.setmode(mode)

    def getGPIOMode(self):
        return RPiIO.getmode()

    def setGPIOWarnings(self, receiveWarnings):
        self.logger.debug(f'set gpio warnings to {receiveWarnings}')
        RPiIO.setwarnings(receiveWarnings)

    def setGPIO(self, channel, IO, initial_state=LOW):
        RPiIO.setup(channel, IO, initial=initial_state)
    
    def setGPIOState(self, channel, state):
        RPiIO.output(channel, state)

class GPIOPin(Enum):
   TOF_XSHUT = 25
   #TODO: complete list