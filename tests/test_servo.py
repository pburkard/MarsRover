import pytest
from math import ceil
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from time import sleep
import sys
sys.path.append("/home/pi/MarsRover/marsrovercore")
from marsrovercore.controllers.servocontroller import ServoController

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 60
sc = ServoController(pca)

def test_servo_mg996r():
    sample_servo = sc.DS2
    test_angle = 120
    # get current angle
    current_angle = ceil(sample_servo.angle)
    # set angle 0
    sample_servo.angle = 0
    sleep(1)
    # set test angle
    sample_servo.angle = test_angle
    sleep(1)
    assert sample_servo.is_at_angle(test_angle)
    # back to start
    sample_servo.angle = current_angle

def test_servo_raw_mg996r_raw():
    from adafruit_motor import servo
    myservo = servo.Servo(pca.channels[2], actuation_range=180, min_pulse=625, max_pulse=2650)
    myservo.angle = 0
    sleep(1)
    myservo.angle = 90
    sleep(1)
    myservo.angle = 180
    sleep(1)
    assert 175 < myservo.angle < 181
    myservo.angle = 90

def test_servo_hd1370a():
    sample_servo = sc.CS1
    test_angle = 120
    # get current angle
    current_angle = ceil(sample_servo.angle)
    # set angle 0
    sample_servo.angle = 0
    sleep(1)
    # set test angle
    sample_servo.angle = test_angle
    sleep(1)
    assert sample_servo.is_at_angle(test_angle)
    # back to start
    sample_servo.angle = current_angle

def test_servo_hd1370a_raw():
    from adafruit_motor import servo
    myservo = servo.Servo(pca.channels[6], actuation_range=180, min_pulse=720, max_pulse=2550)
    myservo.angle = 0
    sleep(1)
    myservo.angle = 90
    sleep(1)
    myservo.angle = 180
    sleep(1)
    assert 175 < myservo.angle < 181
    myservo.angle = 90

@pytest.mark.skip
def test_servo_continuous_raw():
    # sample_servo = sc.CS1
    from adafruit_motor import servo
    pca.frequency = 50
    cs1 = servo.ContinuousServo(pca.channels[11])
    cs1.throttle = -1
    sleep(1)
    cs1.throttle = 1
    sleep(1)   
    cs1.throttle = 0

@pytest.mark.skip
def test_servo_pwm():
    pca.frequency = 60
    on_time_ms = 1
    period_ms = 1.0 / 60 * 1000
    duty_cycle = int(on_time_ms / (period_ms / 0xFFFF))
    pca.channels[11].duty_cycle = duty_cycle

@pytest.mark.skip
# for servo directly connected to RPI
def test_servo_gpio_direct_gpiozero():
    from gpiozero import Servo
    servo = Servo(pin=17)
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)

@pytest.mark.skip
def test_servo_gpio_direct_rpigpio():
    import RPi.GPIO as GPIO
    import time

    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(5) # Initialization
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)

@pytest.mark.skip
def test_servo_gpio_direct_pwmio():
    # SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
    #
    # SPDX-License-Identifier: MIT

    import time
    import board
    import pwmio

    # Initialize PWM output for the servo (on pin D5):
    servo = pwmio.PWMOut(board.D17, frequency=50)


    # Create a function to simplify setting PWM duty cycle for the servo:
    def servo_duty_cycle(pulse_ms, frequency=50):
        period_ms = 1.0 / frequency * 1000.0
        duty_cycle = int(pulse_ms / (period_ms / 65535.0))
        return duty_cycle


    # Main loop will run forever moving between 1.0 and 2.0 mS long pulses:
    servo.duty_cycle = servo_duty_cycle(1)
    sleep(1)
    servo.duty_cycle = servo_duty_cycle(2)
    sleep(1)
