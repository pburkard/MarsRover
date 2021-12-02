import raspberrypi as pi
import RPi.GPIO as io

def InitMotors():
   io.setup(pi.IN1, io.OUT)
   io.setup(pi.IN2, io.OUT)
   io.output(pi.IN1, False)
   io.output(pi.IN2, False)


frontleft_pwm_pin = ENA_2
io.setup(frontleft_pwm_pin, io.OUT)
frontleft_pwm = io.PWM(frontleft_pwm_pin,100)
frontleft_pwm.start(0)
frontleft_pwm.ChangeDutyCycle(0)

def setMotorFrontLeft(power):
   int(power)
   if power > 0:
      print(f'motor front left: forward {power}')
      io.output(frontleft_in1, True)
      io.output(frontleft_in2, False)
      pwm = int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   elif power < 0:
      print(f'motor front left: reverse {power}')
      io.output(frontleft_in1, False)
      io.output(frontleft_in2, True)
      pwm = -int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   else:
      pwm = 0
   
   print(f'pwm: {pwm}')
   frontleft_pwm.ChangeDutyCycle(pwm)   