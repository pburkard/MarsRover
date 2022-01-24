from Adafruit_PCA9685 import PCA9685
import logging
from time import sleep
from marsrover import DriveDirection, WheelPosition
from servocontroller import ServoControllerChannel
from parts.raspberrypi import RaspberryPi
from enum import Enum

class MotorDirection(Enum):
   POSITIVE = 0
   NEGATIVE = 1

class MotorController():
   # The variable duty_cycle specifies the maximum duty cycle of the motors 
   # per 100 Herts. For the speed of the motors the duty cycle always starts 
   # at 0 and ends at a value of 4095 ]0, 4095[.
   DC = 4095

   def __init__(self, raspberrypi: RaspberryPi, pca9685: PCA9685):
      self.logger = logging.getLogger('MarsRover.MotorController')
      self.pca = pca9685
      self.raspberrypi = raspberrypi
   
   def setMotor(self, motor: ServoControllerChannel, rpichannel1: int, rpichannel2: int, speed: float, direction: MotorDirection):
      rpi = self.raspberrypi

      if direction == MotorDirection.POSITIVE:
         rpi.setGPIOState(rpichannel1, rpi.HIGH)
      elif direction == MotorDirection.NEGATIVE:
         rpi.setGPIOState(rpichannel2, rpi.HIGH)
      
      if speed > 0.0 and speed <= 1.0:
         pwm = int(self.DC * speed)
         self.logger.debug(f"set motor {motor.name} to speed: {speed} pwm: {pwm}")
         self.pca.set_pwm(motor.value, False, pwm)
   
   

   def setalllmotors(self, drivedirection: DriveDirection, wheelposition: WheelPosition, speed: float):
      rpi = self.raspberrypi
      mdm1: MotorDirection
      mdm2: MotorDirection
      mdm3: MotorDirection
      mdm4: MotorDirection

      if wheelposition == WheelPosition.HORIZONTAL:
         if drivedirection == DriveDirection.FORWARD:
            mdm1 = MotorDirection.NEGATIVE
            mdm2 = MotorDirection.NEGATIVE
            mdm3 = MotorDirection.POSITIVE
            mdm4 = MotorDirection.POSITIVE
         else:
            mdm1 = MotorDirection.POSITIVE
            mdm2 = MotorDirection.POSITIVE
            mdm3 = MotorDirection.NEGATIVE
            mdm4 = MotorDirection.NEGATIVE
      elif wheelposition == WheelPosition.CIRCULAR:
         if drivedirection == DriveDirection.FORWARD:
            mdm1 = MotorDirection.POSITIVE
            mdm2 = MotorDirection.POSITIVE
            mdm3 = MotorDirection.POSITIVE
            mdm4 = MotorDirection.POSITIVE
         else:
            mdm1 = MotorDirection.NEGATIVE
            mdm2 = MotorDirection.NEGATIVE
            mdm3 = MotorDirection.NEGATIVE
            mdm4 = MotorDirection.NEGATIVE
      elif wheelposition == WheelPosition.VERTICAL:
         if drivedirection == DriveDirection.FORWARD:
            mdm1 = MotorDirection.NEGATIVE
            mdm2 = MotorDirection.POSITIVE
            mdm3 = MotorDirection.NEGATIVE
            mdm4 = MotorDirection.POSITIVE
         else:
            mdm1 = MotorDirection.POSITIVE
            mdm2 = MotorDirection.NEGATIVE
            mdm3 = MotorDirection.POSITIVE
            mdm4 = MotorDirection.NEGATIVE
      
      self.setMotor(ServoControllerChannel.M1, rpi.MC1_IN1, rpi.MC1_IN2, speed, mdm1)
      self.setMotor(ServoControllerChannel.M2, rpi.MC1_IN3, rpi.MC1_IN4, speed, mdm2)
      self.setMotor(ServoControllerChannel.M3, rpi.MC2_IN1, rpi.MC2_IN2, speed, mdm3)
      self.setMotor(ServoControllerChannel.M4, rpi.MC2_IN3, rpi.MC2_IN4, speed, mdm4)

   def dispatchAllMotors(self):
      rpi = self.raspberrypi
      
      rpi.setGPIOState(rpi.MC1_IN1, rpi.LOW)
      rpi.setGPIOState(rpi.MC1_IN2, rpi.LOW)
      rpi.setGPIOState(rpi.MC1_IN3, rpi.LOW)
      rpi.setGPIOState(rpi.MC1_IN4, rpi.LOW)
      rpi.setGPIOState(rpi.MC2_IN1, rpi.LOW)
      rpi.setGPIOState(rpi.MC2_IN2, rpi.LOW)
      rpi.setGPIOState(rpi.MC2_IN3, rpi.LOW)
      rpi.setGPIOState(rpi.MC2_IN4, rpi.LOW)

      self.pca.set_pwm(ServoControllerChannel.M1.value, False, False)
      self.pca.set_pwm(ServoControllerChannel.M2.value, False, False)
      self.pca.set_pwm(ServoControllerChannel.M3.value, False, False)
      self.pca.set_pwm(ServoControllerChannel.M4.value, False, False)