from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from time import sleep

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 60

def move_servo_standalone(to_angle):
    from adafruit_motor import servo

    sample_servo = servo.Servo(pca.channels[5], actuation_range=180, min_pulse=700, max_pulse=2700)
    sample_servo.angle = to_angle
    sleep(1)
    result = sample_servo.angle
    pca.deinit()
    return result

def move_servo(to_angle):
    from marsrovercore.controllers.servocontroller import ServoController

    sc = ServoController(pca)
    sample_servo = sc.DS4
    sample_servo.angle = to_angle
    sleep(1)
    result = sample_servo.angle
    pca.deinit()
    return result

def test_move_servo_to_angle_135():
    test_angle = 135
    precision = 0.5
    assert (test_angle-precision) <= move_servo(test_angle) <= (test_angle+precision)