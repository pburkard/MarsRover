import time
import raspberrypi as pi

def StopSpinMotors():
    print('stop motors')
    # pi.setMotorFrontLeft(0)
    # pi.setMotorFrontRight(0)
    # pi.setMotorRearLeft(0)
    # pi.setMotorRearRight(0)

def Wait(duration):
    print(f'wait for {duration} secs')
    int(duration)
    time.sleep(duration)

def StartUp():
    print('running Startup')
    
def FinishUp():
    print('running FinishUp')
    StopSpinMotors()
    pi.setAngle(90)
    pi.Exit()

def Test():
    # pi.setMotorRearRight(0.1)
    pi.setAngle(180)
    Wait(1)








StartUp()
Test()
FinishUp()

