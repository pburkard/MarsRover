import logging
# import Classes.TSL2591 as LightSensor
import Classes.SGP40 as VOCSensor
import Classes.LTR390 as UVSensor
# import Classes.ICM20948 as MotionSensor
import Classes.BME280 as WeatherSensor

logger = logging.getLogger("MarsRover.EnvironmentController")

bme = WeatherSensor.BME280()
# light = LightSensor.TSL2591()
uv = UVSensor.LTR390()
voc = VOCSensor.SGP40()
# motion = MotionSensor.ICM20948()

def getTemperature():
    return bme.getTemperature()

def getPressure():
    return bme.getPressure()

def getHumidity():
    return bme.getHumidity()

def getUV():
    return uv.getUV()

def getGas():
    return voc.raw()
    # return voc.measureRaw(getTemperature(), getHumidity())
