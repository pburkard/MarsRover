import Adafruit_PCA9685
import logging

class PCA9685():
    def __init__(self, pwmFrequency):
        self.logger = logging.getLogger('MarsRover.PCA9685')
        self.logger.info(f'init {PCA9685.__name__}')
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()
        # PWM frequency set to 60 Hz
        self.setFrequency(pwmFrequency)
    
    def setPWM(self, channel, on, off):
        self.logger.debug(f'set pwm on channel {channel} to {on}, {off}')
        self.pwm.set_pwm(channel, on, off)

    def setFrequency(self, frequency):
        self.logger.info(f'set pwm frequency to {frequency}')
        self.pwm.set_pwm_freq(frequency)

