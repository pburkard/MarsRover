from enum import Enum

class WheelPosition(Enum):
   VERTICAL = 0
   HORIZONTAL = 1
   CIRCLE = 2

class DriveDirection(Enum):
   FORWARD = 0
   REVERSE = 1