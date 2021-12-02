import RPi.GPIO as io
from time import sleep

# General
io.setmode(io.BCM)
io.setwarnings(False)
DC_MAX = 100

ENA = 18
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
ENB = 12

# servo 1
SRV = 24
io.setup(SRV, io.OUT)
io.output(SRV, False)
srv_pwm = io.PWM(SRV, 50)
srv_pwm.start(0)
srv_pwm.ChangeDutyCycle(0)

def test(dc):
   float(dc)
   print(f'dc: {dc}')
   srv_pwm.ChangeDutyCycle(dc)
   sleep(1)

def setAngle(angle):
   print(f'setting angle {angle}')
   test(8.9*(angle / 180) + 4.5)




# # FRONT RIGHT
# frontright_in1 = IN3_2
# frontright_in2 = IN4_2
# io.setup(frontright_in1, io.OUT)
# io.setup(frontright_in2, io.OUT)
# io.output(frontright_in1, False)
# io.output(frontright_in2, False)

# frontright_pwm_pin = ENB_2
# io.setup(frontright_pwm_pin, io.OUT)
# frontright_pwm = io.PWM(frontright_pwm_pin,100)
# frontright_pwm.start(0)
# frontright_pwm.ChangeDutyCycle(0)

# def setMotorFrontRight(power):
#    int(power)
#    if power > 0:
#       print(f'motor front right: forward {power}')
#       io.output(frontright_in1, False)
#       io.output(frontright_in2, True)
#       pwm = int(DC_MAX * power)
#       if pwm > DC_MAX:
#          pwm = DC_MAX
#    elif power < 0:
#       print(f'motor front right: reverse {power}')
#       io.output(rearleft_in1, True)
#       io.output(rearleft_in2, False)
#       pwm = -int(DC_MAX * power)
#       if pwm > DC_MAX:
#          pwm = DC_MAX
#    else:
#       pwm = 0
      
#    print(f'pwm: {pwm}')
#    frontright_pwm.ChangeDutyCycle(pwm)

# # REAR LEFT
# rearleft_in1 = IN1
# rearleft_in2 = IN2
# io.setup(rearleft_in1, io.OUT)
# io.setup(rearleft_in2, io.OUT)
# io.output(rearleft_in1, False)
# io.output(rearleft_in2, False)

# rearleft_pwm_pin = ENA
# io.setup(rearleft_pwm_pin, io.OUT)
# rearleft_pwm = io.PWM(rearleft_pwm_pin,100)
# rearleft_pwm.start(0)
# rearleft_pwm.ChangeDutyCycle(0)

# def setMotorRearLeft(power):
#    int(power)
#    if power > 0:
#       print(f'motor rear left: forward {power}')
#       io.output(rearleft_in1, True)
#       io.output(rearleft_in2, False)
#       pwm = int(DC_MAX * power)
#       if pwm > DC_MAX:
#          pwm = DC_MAX
#    elif power < 0:
#       print(f'motor rear left: reverse {power}')
#       io.output(rearleft_in1, False)
#       io.output(rearleft_in2, True)
#       pwm = -int(DC_MAX * power)
#       if pwm > DC_MAX:
#          pwm = DC_MAX
#    else:
#       pwm = 0
      
#    print(f'pwm: {pwm}')
#    rearleft_pwm.ChangeDutyCycle(pwm)

# # REAR RIGHT
# rearright_in1 = IN3
# rearright_in2 = IN4
# io.setup(rearright_in1, io.OUT)
# io.setup(rearright_in2, io.OUT)
# io.output(rearright_in1, False)
# io.output(rearright_in2, False)

# rearright_pwm_pin = ENB
# io.setup(rearright_pwm_pin, io.OUT)
# rearright_pwm = io.PWM(rearright_pwm_pin,100)
# rearright_pwm.start(0)
# rearright_pwm.ChangeDutyCycle(0)

# def setMotorRearRight(power):
#    int(power)
#    if power > 0:
#       print(f'motor rear right: forward {power}')
#       io.output(rearright_in1, False)
#       io.output(rearright_in2, True)
#       pwm = int(DC_MAX * power)
#       if pwm > DC_MAX:
#          pwm = DC_MAX
#    elif power < 0:
#       print(f'motor rear right: reverse {power}')
#       io.output(rearright_in1, True)
#       io.output(rearright_in2, False)
#       pwm = -int(DC_MAX * power)
#       if pwm > DC_MAX:
#          pwm = DC_MAX
#    else:
#       pwm = 0
      
#    print(f'pwm: {pwm}')
#    rearright_pwm.ChangeDutyCycle(pwm)

# def calibrateServo():
#    print('starting calibrateServo')
#    io.output(SRV, True)
#    dutycicle1 = 5
#    print(f'{dutycicle1}')
#    srv_pwm.ChangeDutyCycle(dutycicle1)
#    sleep(2)
#    dutycycle2 = 7.5
#    print(f'{dutycycle2}')
#    srv_pwm.ChangeDutyCycle(dutycycle2)
#    sleep(2)
#    dutycycle3 = 10
#    print(f'{dutycycle3}')
#    srv_pwm.ChangeDutyCycle(dutycycle3)
#    sleep(2)

   

# def setAngle(angle):
#    print(f'starting setAngle with angle {angle}')
#    duty = angle / 18
#    print(f'duty: {duty}')
#    io.output(SRV, True)
#    srv_pwm.ChangeDutyCycle(duty)
#    sleep(1)
#    io.output(SRV, False)

def Exit():
   print('starting exit')
   # io.output(rearleft_in1, False)
   # io.output(rearleft_in2, False)
   # io.output(rearright_in1, False)
   # io.output(rearright_in2, False)
   # io.output(frontleft_in1, False)
   # io.output(frontleft_in2, False)
   # io.output(frontright_in1, False)
   # io.output(frontright_in2, False)
   io.output(SRV, False)
   io.cleanup()
