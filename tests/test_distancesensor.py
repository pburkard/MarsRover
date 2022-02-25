# import sys
# sys.path.append("/home/pi/MarsRover/marsrovercore")
from marsrovercore.classes.distance_vl53l0x import DistanceSensor
from marsrovercore.classes.gpio import GPIO

def test_distance():
    gpio = GPIO()
    distancesensor = DistanceSensor()
    result = distancesensor.get_distance()
    assert result > 0