import logging
from adafruit_pca9685 import PWMChannel
from adafruit_motor import servo
from time import sleep

class Servo(servo.Servo):
    def __init__(self, name:str, channel: PWMChannel, actuation_range: float, min_pulse: float, max_pulse: float):
        super().__init__(channel, actuation_range=actuation_range, min_pulse=min_pulse, max_pulse=max_pulse)
        self.logger = logging.getLogger(f"MarsRover.{Servo.__name__}.{name}")
        self.name = name

    def set_angle(self, to_angle:float, speed:float = 1):
        if not 0 < speed <= 1:
            raise Exception("speed value not valid")
        self.logger.info(f"set {self.name} to {to_angle}°, speed: {speed}")
        for i in range(to_angle):
            self.angle = i
            sleep(0.05)
