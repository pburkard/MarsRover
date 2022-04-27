from marsrovercore.modules.weather_bme280 import BME280
from marsrovercore.modules.light_tsl2591 import TSL2591
from marsrovercore.modules.uv_ltr390 import LTR390
from marsrovercore.modules.voc_sgp40 import SGP40
from marsrovercore.modules.motion_icm20948 import ICM20948
from marsrovercore.modules.distance_vl53l0x import DistanceSensor

def test_temperature_sensor():
    weather_sensor = BME280(address=0x76, bus=3)
    result = weather_sensor.getTemperature()
    assert 10 < result < 35

def test_humidity_sensor():
    weather_sensor = BME280(address=0x76, bus=3)
    result = weather_sensor.getHumidity()
    assert 30 < result < 60

def test_pressure_sensor():
    weather_sensor = BME280(address=0x76, bus=3)
    result = weather_sensor.getPressure()
    assert 900 < result < 1000

def test_light_sensor():
    light_sensor = TSL2591(address=0x29, bus=3)
    result = light_sensor.get_lux()
    assert 0.0 < result

def test_uv_sensor():
    uv_sensor = LTR390(address=0x53, bus=3)
    result = uv_sensor.getUV()
    assert 0 <= result

def test_motion_sensor():
    motion_sensor = ICM20948(address=0x68, bus=3)
    result = motion_sensor.getdata()
    assert result[0] is not None

# device is dead. Its address is not showing up on the i2c.
# def test_voc_sensor():
#     voc_sensor = SGP40(i2c_address=0x59, i2c_bus_number=3)
#     result = voc_sensor.get_voc_index()

def test_distance():
    distancesensor = DistanceSensor()
    result = distancesensor.get_distance()
    assert 0 <= result <= 8150

