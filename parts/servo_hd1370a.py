import logging
from parts.servo import Servo
from servocontroller import PCA9685

class HD1370A(Servo):

    def __init__(self, name, pca:PCA9685, channel, min, max, mid, rmid, lmid):
        super().__init__(name, pca, channel, min, max, mid)
        self.logger = logging.getLogger(f"MarsRover.HD1370A.{self.name}")
        self.RMID = rmid
        self.LMID = lmid

    def toRMid(self):
        self.logger.debug("move to RMID")
        self.setPWM(False, self.RMID)

    def toLMid(self):
        self.logger.debug("move to LMID")
        self.setPWM(False, self.LMID)