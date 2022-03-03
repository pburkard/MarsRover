import logging
from adafruit_pca9685 import PWMChannel
from adafruit_motor import servo
from time import sleep

class Servo(servo.Servo):
    def __init__(self, name:str, channel: PWMChannel, actuation_range: float, min_pulse: float, max_pulse: float):
        super().__init__(channel, actuation_range=actuation_range, min_pulse=min_pulse, max_pulse=max_pulse)
        self.logger = logging.getLogger(f"MarsRover.{Servo.__name__}.{name}")
        self.name = name

    # error on startup: angle way too high. probably move once with standard angle change, before continue
    # def set_angle(self, to_angle:int, speed_not_implemented:float = 1.0):
    #     if not 0 < speed_not_implemented <= 1:
    #         raise Exception("speed value not valid")
    #     self.logger.info(f"set {self.name} to {to_angle}°, speed: {speed_not_implemented}")
    #     angle_is = int(self.angle)
    #     angle_should = to_angle
    #     if angle_is < angle_should:
    #         step = 1
    #     else: 
    #         step = -1
    #     move = range(angle_is, angle_should, step)
    #     sleeptime = 0.01
    #     for i in move:
    #         self.angle = i
    #         sleep(sleeptime)
    #     angle_offset = self.get_angle_offset(angle_should)
    #     self.logger.debug(f"move complete with offset: {angle_offset}")
    #     return angle_offset

    # def get_angle_offset(self, angle_should):
    #     return angle_should - self.angle

    # def get_sleeptime_from_speed(speed: float):
    #     1.0 == sleep(0)
    #     0.1 == sleep(0.05)
    #     _range = [x / 1000.0 for x in range(50, 0, -5)]
    #     value = 0.1
    #     for i in _range:
            
    #         if value == speed:
    #             return i

    #         value = value+0.1
