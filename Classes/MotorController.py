from Adafruit_PCA9685 import PCA9685
import logging
from time import sleep
from Enums import WheelPosition
from Classes.RaspberryPi import RaspberryPi

class MotorController:
   # The variable duty_cycle specifies the maximum duty cycle of the motors 
   # per 100 Herts. For the speed of the motors the duty cycle always starts 
   # at 0 and ends at a value of 4095 ]0, 4095[.
   DC = 4095
   # MOTOR A - Rear Motors
   MOTOR_A = 0 
   # MOTOR B - Front Motors
   MOTOR_B = 1

   def __init__(self, pca: PCA9685, rpi: RaspberryPi) -> None:
      self.logger = logging.getLogger('MarsRover.MotorController')
      self.pca = pca
      self.rpi = rpi
      
   def _setFrontMotors(self, power):
      if power < 0:
         power = power*-1
      pulse = int(self.DC * power)
      
      if pulse > self.DC:
         pulse = self.DC

      self.logger.debug(f"set front motors to power: {power} pwm: {pulse}")
      self.pca.set_pwm(self.MOTOR_B, False, pulse)

   def _setRearMotors(self, power):
      if power < 0:
         power = power*-1
      pulse = int(self.DC * power)
      
      if pulse > self.DC:
         pulse = self.DC
      
      self.logger.debug(f"set rear motors to power: {power} pwm: {pulse}")
      self.pca.set_pwm(self.MOTOR_A, False, pulse)

   def _dispatchFrontMotors(self):
      self.logger.debug("dispatch front")
      self.pca.set_pwm(self.MOTOR_B, False, False)

   def _dispatchRearMotors(self):
      self.logger.debug("dispatch rear")
      self.pca.set_pwm(self.MOTOR_A, False, False)

   def drive(self, duration, speed, wheelposition: WheelPosition):
      rpi = self.rpi
      self.logger.info(f"drive {duration}s with {speed} speed")
      if wheelposition == WheelPosition.VERTICAL:
         if speed > 0:
            # forward -> pins 6,19 HIGH
            rpi.setOutput(6, rpi.HIGH)
            rpi.setOutput(19, rpi.HIGH)
         else:
            # reverse -> pins 13, 26 HIGH
            rpi.setOutput(13, rpi.HIGH)
            rpi.setOutput(26, rpi.HIGH)
         
      elif wheelposition == WheelPosition.HORIZONTAL:
         if speed > 0:
            # left -> pins 13,19 HIGH
            rpi.setOutput(13, rpi.HIGH)
            rpi.setOutput(19, rpi.HIGH)
         else:
            # right -> pins 6,26 HIGH
            rpi.setOutput(6, rpi.HIGH)
            rpi.setOutput(26, rpi.HIGH)
            

      self._setFrontMotors(speed)
      self._setRearMotors(speed)
      sleep(duration)
      rpi.setOutput(6, rpi.LOW)
      rpi.setOutput(19, rpi.LOW)
      rpi.setOutput(13, rpi.LOW)
      rpi.setOutput(26, rpi.LOW)
      self._dispatchFrontMotors()
      self._dispatchRearMotors()