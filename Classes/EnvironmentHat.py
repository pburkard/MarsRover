import logging
from Classes.TSL2591 import TSL2591
from Classes.SGP40 import SGP40
from Classes.LTR390 import LTR390
from Classes.ICM20948 import ICM20948
from Classes.BME280 import BME280

class EnvironmentHat():
    def __init__(self) -> None:
        self.logger = logging.getLogger("MarsRover.EnvironmentHat")
        
        self.I2cBus = 3
        self.weatherSensor = BME280(bus=self.I2cBus)
        self.lightSensor = TSL2591(bus=self.I2cBus)
        self.uvSensor = LTR390(bus=self.I2cBus)
        self.vocSensor = SGP40(bus=self.I2cBus)
        self.motionSensor = ICM20948(bus=self.I2cBus)

    def getTemperature(self):
        return self.weatherSensor.getTemperature()

    def getPressure(self):
        return self.weatherSensor.getPressure()

    def getHumidity(self):
        return self.weatherSensor.getHumidity()

    def getUV(self):
        return self.uvSensor.getUV()

    def getGas(self):
        return self.vocSensor.raw()
        # voc.measureRaw(getTemperature(), getHumidity())

    #TODO: implement motion sensing

    def takeEnvironmentMeasurement(self):
        self.getTemperature()
        self.getPressure()
        self.getHumidity()
        self.getUV()
        self.getGas()