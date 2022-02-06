from enum import Enum

class WheelPosition(Enum):
   VERTICAL = 0
   HORIZONTAL = 1
   CIRCULAR = 2

class DriveDirection(Enum):
   FORWARD = 1
   REVERSE = 2
   TURN_LEFT = 1
   TURN_RIGHT = 2

class StartMode(Enum):
   AUTONOMOUS = 0
   WEBCONTROL = 1
   TESTBED = 2

class ServoDriverChannel(Enum):
   M1 = 0
   M2 = 1
   DS4 = 2
   DS3 = 3
   DS2 = 4
   DS1 = 5
   CS1 = 6
   M3 = 8
   M4 = 9

class MotorDirection(Enum):
   POSITIVE = 0
   NEGATIVE = 1

class Pin(Enum):
    I2C_BUS_0_SDA=2
    I2C_BUS_0_SCL=3
    MC1_IN1=6
    ENVH_LIGHT=10
    MC2_IN1=12
    MC1_IN2=13
    MC2_IN2=16
    MC1_IN3=19
    MC2_IN3=20
    MC2_IN4=21
    I2C_BUS_3_SDA=23
    I2C_BUS_3_SCL=24
    DISTANCE_XSHUT=25
    MC1_IN4=26
    
class PinSignalState(Enum):
    LOW = 0
    HIGH = 1

class PinSignalDirection(Enum):
    OUTPUT = 0
    INPUT = 1