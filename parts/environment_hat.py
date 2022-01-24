import logging
from parts.light_tsl2591 import TSL2591
from parts.voc_sgp40 import SGP40
from parts.uv_ltr390 import LTR390
from parts.motion_icm20948 import ICM20948
from parts.weather_bme280 import BME280

class EnvironmentHat():
    def __init__(self) -> None:
        self.logger = logging.getLogger("MarsRover.EnvironmentHat")
        
        self.I2cBus = 3
        self.weatherSensor = BME280(bus=self.I2cBus)
        self.lightSensor = TSL2591(bus=self.I2cBus)
        self.uvSensor = LTR390(bus=self.I2cBus)
        self.vocSensor = SGP40(bus=self.I2cBus)
        self.motionSensor = ICM20948(bus=self.I2cBus)

    def get_lux(self) -> float:
        return self.lightSensor.Lux()

    def get_temperature(self) -> float:
        return self.weatherSensor.getTemperature()

    def get_pressure(self) -> float:
        return self.weatherSensor.getPressure()

    def get_humidity(self) -> float:
        return self.weatherSensor.getHumidity()

    def get_uv(self) -> float:
        return self.uvSensor.getUV()
    
    def get_voc(self) -> int:
        temp = int(round(self.get_temperature(), 0))
        hum = int(round(self.get_humidity(), 0))
        # self.vocSensor.get_voc_index(temp, hum)
        return 100

    #TODO: implement motion sensing

    def get_all_measures(self, round_decimal_place: int = None) -> dict:
        temp = self.get_temperature()
        hum = self.get_humidity()
        press = self.get_pressure()
        uv = self.get_uv()
        lux = self.get_lux()
        voc = self.get_voc()
        measures_dict = {
            "temperature": temp,
            "humidity": hum,
            "pressure": press,
            "uv": uv,
            "light": lux,
            "voc": voc
        }
        if round_decimal_place >= 0:
            for key, value in measures_dict.items():
                try:
                    measures_dict[key] = round(value, round_decimal_place)
                except:
                    self.logger.warning(f"failed to round {key}: {value}")
        return measures_dict