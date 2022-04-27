from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from time import sleep
from marsrovercore.controllers.servocontroller import ServoController
from marsrovercore.enums import WheelPosition

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 60
sc = ServoController(pca)

def test_wheelpositon_circular():
    sc.set_drive_servos(WheelPosition.CIRCULAR)

def test_wheelpositon_vertical():
    sc.set_drive_servos(WheelPosition.VERTICAL)

def test_wheelpositon_horizontal():
    sc.set_drive_servos(WheelPosition.HORIZONTAL)