import logging
from modules.servo import Servo
from controllers.servocontroller import PCA9685, ServoDriverChannel

class HD1370A(Servo):

    def __init__(self, name:str, pca:PCA9685, channel:ServoDriverChannel, min, max, mid, rmid, lmid):
        super().__init__(name, pca, channel, min, max, mid)
        self.logger = logging.getLogger(f"MarsRover.HD1370A.{self.name}")
        self.RMID = rmid
        self.LMID = lmid

    def to_rmid(self):
        self.logger.debug("move to mid right")
        self.setPWM(False, self.RMID)

    def to_lmid(self):
        self.logger.debug("move to mid left")
        self.setPWM(False, self.LMID)