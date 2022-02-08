from Adafruit_PCA9685 import PCA9685
import logging
from time import sleep
from marsrovercore.enums import WheelPosition, ServoDriverChannel

class ServoController():
    MOVE_TIME = 1

    def __init__(self, pca9685: PCA9685):
        self.logger = logging.getLogger('MarsRover.ServoController')
        from classes.servo_hd1370a import HD1370A
        from classes.servo_mg996r import MG996R
        # drive servo
        self.DS1 = MG996R("DS1", pca9685, ServoDriverChannel.DS1, mid=407, min=155, max=645)
        self.DS2 = MG996R("DS2", pca9685, ServoDriverChannel.DS2, min=160, mid=406, max=660)
        self.DS3 = MG996R("DS3", pca9685, ServoDriverChannel.DS3, min=170, mid=410)
        self.DS4 = MG996R("DS4", pca9685, ServoDriverChannel.DS4, mid=405)
        # camera servo
        self.CS1 = HD1370A("CS1", pca9685, ServoDriverChannel.CS1, 230, 690, 450, rmid=550, lmid=350)

    def dispatch_drive_servos(self):
        self.DS1.dispatch()
        self.DS2.dispatch()
        self.DS3.dispatch()
        self.DS4.dispatch()
    
    def set_drive_servos(self, position: WheelPosition):
        self.logger.debug(f"set driveservos to {position.name}")
        if position == WheelPosition.VERTICAL:
            self.DS1.to_mid()
            self.DS2.to_mid()
            self.DS3.to_mid()
            self.DS4.to_mid()
            sleep(self.MOVE_TIME)
        elif position == WheelPosition.HORIZONTAL:
            self.DS1.to_max()
            self.DS2.to_min()
            self.DS3.to_min()
            self.DS4.to_max()
            sleep(self.MOVE_TIME)
        elif position == WheelPosition.CIRCULAR:
            self.DS1.custom_pwm(550)
            self.DS2.custom_pwm(250)
            self.DS3.custom_pwm(250)
            self.DS4.custom_pwm(550)
            sleep(self.MOVE_TIME)