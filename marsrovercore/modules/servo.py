import logging
from Adafruit_PCA9685 import PCA9685
from marsrovercore.controllers.servocontroller import ServoDriverChannel

class Servo:
    def __init__(self, name:str, pca:PCA9685, servodriver_channel:ServoDriverChannel, min, max, mid):
        self.logger = logging.getLogger(f"MarsRover.{Servo.__name__}.{name}")
        self.name = name
        self.pca = pca
        self.CHANNEL = servodriver_channel
        self.MIN = min
        self.MAX = max
        self.MID = mid

    def setPWM(self, on, off):
        # Thought for potential angle control

        # pulse_length = 1000000    # 1,000,000 us per second
        # pulse_length //= pwmFrequency
        # logger.debug(f'{pulse_length}us per period')
        # pulse_length //= 4096     # 12 bits of resolution
        # logger.debug(f'{pulse_length}us per bit')
        # pulse *= 1000
        # pulse //= pulse_length
        
        # for angle in range(0, off, 20):  # 0 - 180 degrees, 5 degrees at a time.
        #     self.pca.setPWM(self.CHANNEL, 0, angle)
        #     time.sleep(0.05)
        #     self.pca.setPWM(self.CHANNEL, 0, 0)

        self.logger.debug(f'set pwm on channel {self.CHANNEL.value} ({self.CHANNEL.name}) to {on}, {off}')
        self.pca.set_pwm(self.CHANNEL.value, on, off)

    def to_min(self):
        self.logger.debug("move to MIN")
        self.setPWM(False, self.MIN)

    def to_max(self):
        self.logger.debug("move to MAX")
        self.setPWM(False, self.MAX)

    def to_mid(self):
        self.logger.debug("move to MID")
        self.setPWM(False, self.MID)
    
    def custom_pwm(self, pwm: int):
        self.logger.debug(f"move to {pwm}")
        self.setPWM(False, pwm)

    def dispatch(self):
        self.logger.debug(f"dispatch")
        self.setPWM(False, False)
