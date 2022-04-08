from math import ceil
from adafruit_pca9685 import PCA9685
import marsrovercore.logginghelper as logginghelper
from controllers.servocontroller import ServoDriverChannel
from marsrovercore.modules.gpio import GPIO
from marsrovercore.enums import RotationDirection, ServoDriverChannel, DriveDirection, WheelPosition, Pin, PinSignalState

class MotorController():
   DC_MAX = 0xFFFF

   def __init__(self, gpio: GPIO, pca9685: PCA9685):
      self.logger = logginghelper.get_logger('MotorController')
      self.pca = pca9685
      self.gpio = gpio
   
   def set_gpio_motor_driver(self, rotation_direction: RotationDirection, motordriver_IN_1:Pin, motordriver_IN_2:Pin):
      # open output from gpio's for direction on motor driver boards
      if rotation_direction == RotationDirection.POSITIVE:
         self.gpio.set_signal_state(motordriver_IN_1, PinSignalState.HIGH)
      else:
         # rotation direction NEGATIVE
         self.gpio.set_signal_state(motordriver_IN_2, PinSignalState.HIGH)

   def set_motor_duty_cicle(self, channel:ServoDriverChannel, dc:int):
      # pwm signal from pca9685
      self.logger.debug(f"set motor {channel.name} pwm: {dc}")
      self.pca.channels[channel.value].duty_cycle = dc

   def get_dc_from_speed(self, speed:float) -> int:
      if 0.0 < speed <= 1.0:
         return ceil(self.DC_MAX * speed)
      self.logger.error(f"0.0 < speed <= 1.0. Given value: {speed}")

   def set_motor(self, channel: ServoDriverChannel, motordriver_IN_1:Pin, 
      motordriver_IN_2:Pin, dc: int, rotation_direction: RotationDirection):
      self.set_motor_duty_cicle(channel, dc)
      self.set_gpio_motor_driver(rotation_direction, motordriver_IN_1, motordriver_IN_2)

   def get_rotation_direction(self, wheelposition:WheelPosition, drivedirection:DriveDirection):
      rotation_direction_m1 = RotationDirection.NEGATIVE
      rotation_direction_m2 = RotationDirection.POSITIVE
      rotation_direction_m3 = RotationDirection.NEGATIVE
      rotation_direction_m4 = RotationDirection.POSITIVE

      if wheelposition == WheelPosition.HORIZONTAL:
         if drivedirection == DriveDirection.FORWARD:
            rotation_direction_m1 = RotationDirection.NEGATIVE
            rotation_direction_m2 = RotationDirection.NEGATIVE
            rotation_direction_m3 = RotationDirection.POSITIVE
            rotation_direction_m4 = RotationDirection.POSITIVE
         else:
            rotation_direction_m1 = RotationDirection.POSITIVE
            rotation_direction_m2 = RotationDirection.POSITIVE
            rotation_direction_m3 = RotationDirection.NEGATIVE
            rotation_direction_m4 = RotationDirection.NEGATIVE
      elif wheelposition == WheelPosition.CIRCULAR:
         if drivedirection == DriveDirection.FORWARD:
            rotation_direction_m1 = RotationDirection.POSITIVE
            rotation_direction_m2 = RotationDirection.POSITIVE
            rotation_direction_m3 = RotationDirection.POSITIVE
            rotation_direction_m4 = RotationDirection.POSITIVE
         else:
            rotation_direction_m1 = RotationDirection.NEGATIVE
            rotation_direction_m2 = RotationDirection.NEGATIVE
            rotation_direction_m3 = RotationDirection.NEGATIVE
            rotation_direction_m4 = RotationDirection.NEGATIVE
      elif wheelposition == WheelPosition.VERTICAL:
         if drivedirection == DriveDirection.FORWARD:
            rotation_direction_m1 = RotationDirection.NEGATIVE
            rotation_direction_m2 = RotationDirection.POSITIVE
            rotation_direction_m3 = RotationDirection.NEGATIVE
            rotation_direction_m4 = RotationDirection.POSITIVE
         else:
            rotation_direction_m1 = RotationDirection.POSITIVE
            rotation_direction_m2 = RotationDirection.NEGATIVE
            rotation_direction_m3 = RotationDirection.POSITIVE
            rotation_direction_m4 = RotationDirection.NEGATIVE
      
      return (rotation_direction_m1, rotation_direction_m2, rotation_direction_m3, rotation_direction_m4)

   def set_all_motors(self, drivedirection: DriveDirection, wheelposition: WheelPosition, speed: float):
      dc = self.get_dc_from_speed(speed)
      rotation_directions = self.get_rotation_direction(wheelposition, drivedirection)
      self.set_motor(ServoDriverChannel.M1, Pin.MD1_IN1, Pin.MD1_IN2, dc, rotation_directions[0])
      self.set_motor(ServoDriverChannel.M2, Pin.MD1_IN3, Pin.MD1_IN4, dc, rotation_directions[1])
      self.set_motor(ServoDriverChannel.M3, Pin.MD2_IN1, Pin.MD2_IN2, dc, rotation_directions[2])
      self.set_motor(ServoDriverChannel.M4, Pin.MD2_IN3, Pin.MD2_IN4, dc, rotation_directions[3])

   def dispatch_all(self):
      gpio = self.gpio
      # set duty cicle to 0 on pca9685
      self.pca.channels[ServoDriverChannel.M1.value].duty_cycle = 0
      self.pca.channels[ServoDriverChannel.M2.value].duty_cycle = 0
      self.pca.channels[ServoDriverChannel.M3.value].duty_cycle = 0
      self.pca.channels[ServoDriverChannel.M4.value].duty_cycle = 0
      # set gpio's to low for motor drivers
      # motor driver 1
      gpio.set_signal_state(Pin.MD1_IN1, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MD1_IN2, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MD1_IN3, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MD1_IN4, PinSignalState.LOW)
      # motor driver 2
      gpio.set_signal_state(Pin.MD2_IN1, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MD2_IN2, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MD2_IN3, PinSignalState.LOW)
      gpio.set_signal_state(Pin.MD2_IN4, PinSignalState.LOW)

      