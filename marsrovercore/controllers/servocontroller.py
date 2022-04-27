from adafruit_pca9685 import PCA9685
import logging
from time import sleep
from marsrovercore.enums import WheelPosition, ServoDriverChannel
from marsrovercore.modules.servo import Servo

class ServoController():
    MOVE_TIME = 1

    def __init__(self, pca9685: PCA9685):
        self.logger = logging.getLogger('MarsRover.ServoController')
        # drive servo MG996R
        self.DS1 = Servo(ServoDriverChannel.DS1.name, pca9685.channels[ServoDriverChannel.DS1.value], actuation_range=180, min_pulse=625, max_pulse=2650)
        self.DS2 = Servo(ServoDriverChannel.DS2.name, pca9685.channels[ServoDriverChannel.DS2.value], actuation_range=180, min_pulse=625, max_pulse=2650)
        self.DS3 = Servo(ServoDriverChannel.DS3.name, pca9685.channels[ServoDriverChannel.DS3.value], actuation_range=180, min_pulse=625, max_pulse=2650)
        self.DS4 = Servo(ServoDriverChannel.DS4.name, pca9685.channels[ServoDriverChannel.DS4.value], actuation_range=180, min_pulse=625, max_pulse=2650)
        # camera servo HD1370A
        self.CS1 = Servo(ServoDriverChannel.CS1.name, pca9685.channels[ServoDriverChannel.CS1.value], actuation_range=180, min_pulse=720, max_pulse=2550)
    
    def set_drive_servos(self, position: WheelPosition):
        self.logger.debug(f"set driveservos to {position.name}")
        if position == WheelPosition.VERTICAL:
            self.DS1.angle = 90
            self.DS2.angle = 90
            self.DS3.angle = 90
            self.DS4.angle = 90
            sleep(self.MOVE_TIME)
        elif position == WheelPosition.HORIZONTAL:
            self.DS1.angle = 180
            self.DS2.angle = 0
            self.DS3.angle = 0
            self.DS4.angle = 180
            sleep(self.MOVE_TIME)
        elif position == WheelPosition.CIRCULAR:
            self.DS1.angle = 135
            self.DS2.angle = 45
            self.DS3.angle = 45
            self.DS4.angle = 135
            sleep(self.MOVE_TIME)
