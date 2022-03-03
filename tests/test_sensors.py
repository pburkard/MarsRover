from marsrovercore.controllers.sensorcontroller import SensorController

sc = SensorController(i2c_bus_number=3)

def test_temperature_sensor():
    assert sc.get_temperature() > 0.0

def test_distance_sensor():
    assert sc.get_distance_front() > 0.0

def test_humidity_sensor():
    assert sc.get_humidity() > 0.0

def test_light_sensor():
    assert sc.get_lux() > 0.0