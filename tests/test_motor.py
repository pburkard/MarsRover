from math import ceil
from marsrovercore.controllers.motorcontroller import MotorController
from marsrovercore.enums import DriveDirection, RotationDirection, ServoDriverChannel, WheelPosition, Pin
from time import sleep
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from marsrovercore.modules.gpio import GPIO

def test_motor():
    test_channel = ServoDriverChannel.M1
    test_speed = 0.5
    
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c, address=0x41)
    pca.frequency = 60
    gpio = GPIO()
    mc = MotorController(gpio, pca)
    mc.set_motor(test_channel, Pin.MD1_IN1, Pin.MD1_IN2, mc.get_dc_from_speed(test_speed), RotationDirection.NEGATIVE)
    sleep(1)
    expected_dc = ceil(test_speed * mc.DC_MAX)
    assert pca.channels[test_channel.value].duty_cycle == expected_dc
    mc.dispatch_all()
    pca.deinit()

    

    # from marsrovercore.enums import MotorDirection, ServoDriverChannel, DriveDirection, WheelPosition, Pin, PinSignalState
    # gpio.set_signal_state(Pin.MC1_IN2, PinSignalState.HIGH)
    # pca.channels[0].duty_cycle = 0xFFFF
    # sleep(1)
    # pca.channels[0].duty_cycle = 0
    # gpio.set_signal_state(Pin.MC1_IN2, PinSignalState.LOW)
    # pca.deinit()
