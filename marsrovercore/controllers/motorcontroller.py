from Adafruit_PCA9685 import PCA9685
import logging
from time import sleep
from controllers.servocontroller import ServoDriverChannel
from marsrovercore.modules.gpio import GPIO
from marsrovercore.enums import MotorDirection, ServoDriverChannel, DriveDirection, WheelPosition, Pin, PinSignalState

class MotorController():
   # The variable duty_cycle specifies the maximum duty cycle of the motors 
   # per 100 Herts. For the speed of the motors the duty cycle always starts 
   # at 0 and ends at a value of 4095 ]0, 4095[.
   DC = 4095

   def __init__(self, gpio: GPIO, pca9685: PCA9685):
      self.logger = logging.getLogger('MarsRover.MotorController')
      self.pca = pca9685
      self.gpio = gpio
   
   def set_motor(self, motor: ServoDriverChannel, motordriver_IN1:Pin, motordriver_IN2:Pin, speed: float, direction: MotorDirection):
      gpio = self.gpio
      if speed <= 0.0 and speed > 1.0:
         self.logger.error(f"speed value has to be >0.0 and <=1.0. Given value: {speed}")
      if direction == MotorDirection.POSITIVE:
         gpio.set_signal_state(motordriver_IN1, PinSignalState.HIGH)
      else:
         # motordirection NEGATIVE
         gpio.set_signal_state(motordriver_IN2, PinSignalState.HIGH)
      pwm = int(self.DC * speed)
      self.logger.debug(f"set motor {motor.name} to speed: {speed} pwm: {pwm}")
      self.pca.set_pwm(motor.value, False, pwm)

   def set_all_motors(self, drivedirection: DriveDirection, wheelposition: WheelPosition, speed: float):
      # motor driver motor x
      mdm1: MotorDirection = MotorDirection.NEGATIVE
      mdm2: MotorDirection = MotorDirection.POSITIVE
      mdm3: MotorDirection = MotorDirection.NEGATIVE
      mdm4: MotorDirection = MotorDirection.POSITIVE

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
      
      self.set_motor(ServoDriverChannel.M1, Pin.MC1_IN1, Pin.MC1_IN2, speed, mdm1)
      self.set_motor(ServoDriverChannel.M2, Pin.MC1_IN3, Pin.MC1_IN4, speed, mdm2)
      self.set_motor(ServoDriverChannel.M3, Pin.MC2_IN1, Pin.MC2_IN2, speed, mdm3)
      self.set_motor(ServoDriverChannel.M4, Pin.MC2_IN3, Pin.MC2_IN4, speed, mdm4)

   def dispatch_all(self):
      gpio = self.gpio
      
      gpio.set_signal_state(Pin.MC1_IN1, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MC1_IN2, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MC1_IN3, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MC1_IN4, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MC2_IN1, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MC2_IN2, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MC2_IN3, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MC2_IN4, PinSignalState.LOW)

      self.pca.set_pwm(ServoDriverChannel.M1.value, False, False)
      self.pca.set_pwm(ServoDriverChannel.M2.value, False, False)
      self.pca.set_pwm(ServoDriverChannel.M3.value, False, False)
      self.pca.set_pwm(ServoDriverChannel.M4.value, False, False)