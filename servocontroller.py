from Adafruit_PCA9685 import PCA9685
from parts.servo_hd1370a import HD1370A
from parts.servo_mg996r import MG996R
import logging
from time import sleep
from enum import Enum
from marsrover import WheelPosition

class ServoController():
    MOVE_TIME = 1

    def __init__(self, pca9685: PCA9685):
        self.logger = logging.getLogger('MarsRover.ServoController')
        # drive servo
        self.DS1 = MG996R("DS1", pca9685, 5, mid=408, min=155)
        self.DS2 = MG996R("DS2", pca9685, 4, mid=408, max=660)
        self.DS3 = MG996R("DS3", pca9685, 3, mid=420)
        self.DS4 = MG996R("DS4", pca9685, 2, mid=410)
        # camera servo
        self.CS1 = HD1370A("CS1", pca9685, 6, 230, 690, 450, rmid=550, lmid=350)

    def dispatchdriveservos(self):
        self.DS1.dispatch()
        self.DS2.dispatch()
        self.DS3.dispatch()
        self.DS4.dispatch()
    
    def setdriveservos(self, position: WheelPosition):
        if position == WheelPosition.VERTICAL:
            self.DS1.toMid()
            self.DS2.toMid()
            self.DS3.toMid()
            self.DS4.toMid()
            sleep(self.MOVE_TIME)
        elif position == WheelPosition.HORIZONTAL:
            self.DS1.toMax()
            self.DS2.toMin()
            self.DS3.toMin()
            self.DS4.toMax()
            sleep(self.MOVE_TIME)
        elif position == WheelPosition.CIRCULAR:
            self.DS1.toCustomPWM(550)
            self.DS2.toCustomPWM(250)
            self.DS3.toCustomPWM(250)
            self.DS4.toCustomPWM(550)
            sleep(self.MOVE_TIME)

class ServoControllerChannel(Enum):
   M1 = 0
   M2 = 1
   #TODO: complete list
   M3 = 8
   M4 = 9
