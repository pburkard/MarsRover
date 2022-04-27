from math import ceil
from marsrovercore.controllers.motorcontroller import MotorController
from marsrovercore.controllers.servocontroller import ServoController
from marsrovercore.enums import DriveDirection, WheelPosition
from time import sleep
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from marsrovercore.modules.gpio import GPIO

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 60
gpio = GPIO()
mc = MotorController(gpio, pca)
sc = ServoController(pca)

def test_drive_forward():
    test_speed = 0.5
    test_wheelposition = WheelPosition.VERTICAL
    test_drivedirection = DriveDirection.FORWARD
    test_duration = 1

    sc.set_drive_servos(test_wheelposition)
    mc.set_all_motors(test_drivedirection, test_wheelposition, test_speed)
    sleep(test_duration)
    mc.stop_all_motors()
    mc.dispatch_all()
    pca.deinit()

def test_drive_reverse():
    test_speed = 0.5
    test_wheelposition = WheelPosition.VERTICAL
    test_drivedirection = DriveDirection.REVERSE
    test_duration = 1

    sc.set_drive_servos(test_wheelposition)
    mc.set_all_motors(test_drivedirection, test_wheelposition, test_speed)
    sleep(test_duration)
    mc.stop_all_motors()
    mc.dispatch_all()
    pca.deinit()