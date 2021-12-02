from Classes.PCA9685 import PCA9685
import logging
import time

logger = logging.getLogger('MarsRover.ServoController')

pwmFrequency = 60
pca = PCA9685(pwmFrequency)
# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096
servo_mid = 400

# Helper function to make setting a servo pulse width simpler.
def setServoPulse(channel, pulse):
    # pulse_length = 1000000    # 1,000,000 us per second
    # pulse_length //= pwmFrequency
    # logger.debug(f'{pulse_length}us per period')
    # pulse_length //= 4096     # 12 bits of resolution
    # logger.debug(f'{pulse_length}us per bit')
    # pulse *= 1000
    # pulse //= pulse_length
    pca.setPWM(channel, False, pulse)

def leftToMin():
    setServoPulse(4, servo_max)
    setServoPulse(5, servo_max)

def leftToMax():
    setServoPulse(4, servo_min)
    setServoPulse(5, servo_min)

def rightToMin():
    setServoPulse(2, servo_min)
    setServoPulse(3, servo_min)

def rightToMax():
    setServoPulse(2, servo_max)
    setServoPulse(3, servo_max)

def allToCenter():
    setServoPulse(2, servo_mid + 10)
    setServoPulse(3, servo_mid + 20)
    setServoPulse(4, servo_mid + 8)
    setServoPulse(5, servo_mid + 8)

def dispatchServos():
    logger.debug(f'start {dispatchServos.__name__}')
    setServoPulse(2, False)
    setServoPulse(3, False)
    setServoPulse(4, False)
    setServoPulse(5, False)

def moveHD1370A(pulse):
    setServoPulse(6, pulse)

def dispatchCamServo():
    logger.debug(f'start {dispatchCamServo.__name__}')
    setServoPulse(6, False)