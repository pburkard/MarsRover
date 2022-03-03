from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from time import sleep

def move_servo(to_angle):
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c, address=0x41)
    pca.frequency = 60
    from marsrovercore.controllers.servocontroller import ServoController
    sc = ServoController(pca)
    sample_servo = sc.DS2
    sample_servo.angle = 0
    sleep(1)
    sample_servo.angle = to_angle
    sleep(1)
    result = sample_servo.angle
    pca.deinit()
    return result

def is_within_precision(precision_degrees, test_angle, result_angle):
    return (test_angle-precision_degrees) <= result_angle <= (test_angle+precision_degrees)

def test_move_servo():
    test_angle = 90
    result_angle = move_servo(test_angle)
    assert is_within_precision(2, test_angle, result_angle)