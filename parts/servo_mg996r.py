import logging
from parts.servo import Servo
from servocontroller import PCA9685

class MG996R(Servo):
    def __init__(self, name, pca:PCA9685, channel, min=150, max=650, mid=400):
        super().__init__(name, pca, channel, min, max, mid)
        self.logger = logging.getLogger(f"MarsRover.MG996R.{self.name}")