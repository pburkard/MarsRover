from Adafruit_PCA9685 import PCA9685
from Classes.HD1370A import HD1370A
from Classes.MG996R import MG996R
import logging
from time import sleep

class ServoController():
    MOVE_TIME = 0.5

    def __init__(self, pca: PCA9685):
        self.logger = logging.getLogger('MarsRover.ServoController')
        
        self.pca = pca

        self.DS1 = MG996R("DS1", self.pca, 5, mid=408, min=155)
        self.DS2 = MG996R("DS2", self.pca, 4, mid=408, max=660)
        self.DS3 = MG996R("DS3", self.pca, 3, mid=420)
        self.DS4 = MG996R("DS4", self.pca, 2, mid=410)
        self.CS1 = HD1370A("CS1", self.pca, 6, 230, 690, 450, rmid=550, lmid=350)

    def dispatchDriveServos(self):
        self.DS1.dispatch()
        self.DS2.dispatch()
        self.DS3.dispatch()
        self.DS4.dispatch()
    
    def rotateWheelsHorizontal(self):
        self.DS1.toMin()
        self.DS2.toMax()
        self.DS3.toMin()
        self.DS4.toMax()
        sleep(self.MOVE_TIME)
    
    def rotateWheelsVertical(self):
        self.DS1.toMid()
        self.DS2.toMid()
        self.DS3.toMid()
        self.DS4.toMid()
        sleep(self.MOVE_TIME)
    
    # def setPWM(self, channel, on, off):
    #     self.logger.debug(f'set pwm on channel {channel} to {on}, {off}')
    #     self.pca.set_pwm(channel, on, off)

