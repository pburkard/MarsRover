from marsrovercore.modules.distance_vl53l0x import DistanceSensor
from marsrovercore.modules.gpio import GPIO

def test_distance():
    gpio = GPIO()
    distancesensor = DistanceSensor()
    result = distancesensor.get_distance()
    assert result > 0