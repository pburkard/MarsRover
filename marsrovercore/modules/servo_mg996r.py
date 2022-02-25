import logging
from modules.servo import Servo
from controllers.servocontroller import PCA9685, ServoDriverChannel

class MG996R(Servo):
    def __init__(self, name:str, pca:PCA9685, channel:ServoDriverChannel, min=150, max=650, mid=400):
        super().__init__(name, pca, channel, min, max, mid)
        self.logger = logging.getLogger(f"MarsRover.MG996R.{self.name}")