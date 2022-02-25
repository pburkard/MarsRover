from marsrovercore.controllers.motorcontroller import MotorController
from marsrovercore.enums import DriveDirection, WheelPosition
from time import sleep
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

def test_motor():
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    mc = MotorController(pca)

    mc.set_all_motors(DriveDirection.FORWARD, WheelPosition.VERTICAL, 0.5)
    sleep(1)
    mc.dispatch_all()