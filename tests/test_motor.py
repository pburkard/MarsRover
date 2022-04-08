from marsrovercore.controllers.motorcontroller import MotorController
from marsrovercore.enums import DriveDirection, WheelPosition
from time import sleep
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from marsrovercore.modules.gpio import GPIO
# from Adafruit_PCA9685 import PCA9685
from adafruit_motor import motor

def test_motor():
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c, address=0x41)
    pca.frequency = 60
    gpio = GPIO()
    mc = MotorController(gpio, pca)
    
    mc.set_all_motors(DriveDirection.FORWARD, WheelPosition.VERTICAL, 0.5)
    sleep(5)
    mc.dispatch_all()
    pca.deinit()

    # from marsrovercore.enums import MotorDirection, ServoDriverChannel, DriveDirection, WheelPosition, Pin, PinSignalState
    # gpio.set_signal_state(Pin.MC1_IN2, PinSignalState.HIGH)
    # pca.channels[0].duty_cycle = 0xFFFF
    # sleep(1)
    # pca.channels[0].duty_cycle = 0
    # gpio.set_signal_state(Pin.MC1_IN2, PinSignalState.LOW)
    # pca.deinit()
