from Classes.PCA9685 import PCA9685
import logging

logger = logging.getLogger('MarsRover.MotorController')
pca = PCA9685(60)
# The variable duty_cycle specifies the maximum duty cycle of the motors 
# per 100 Herts. For the speed of the motors the duty cycle always starts 
# at 0 and ends at a value of 4095 ]0, 4095[.
motorDutyCycle = 4095

def setFrontMotors(power):
   pulse = int(motorDutyCycle * power)
   
   if pulse > motorDutyCycle:
        pulse = motorDutyCycle
   
   logger.debug(f"set front motors to\n power: {power}\n pwm: {pulse}")
   pca.setPWM(1, False, pulse)

def setRearMotors(power):
   pulse = int(motorDutyCycle * power)
   
   if pulse > motorDutyCycle:
        pulse = motorDutyCycle
   
   logger.debug(f"set rear motors to\n power: {power}\n pwm: {pulse}")
   pca.setPWM(0, False, pulse)

def dispatchMotors():
   logger.info(f'start {dispatchMotors.__name__}')
   pca.setPWM(0, False, False)
   pca.setPWM(1, False, False)