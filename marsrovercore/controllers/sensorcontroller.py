import logging
from threading import Thread
from time import sleep
from classes.light_tsl2591 import TSL2591
# from classes.voc_sgp40 import SGP40
from classes.uv_ltr390 import LTR390
from classes.motion_icm20948 import ICM20948
from classes.weather_bme280 import BME280
from classes.distance_vl53l0x import DistanceSensor
from marsrovercore.marsrover import MarsRover

class SensorController():
    def __init__(self, i2c_bus: int) -> None:
        self.logger = logging.getLogger("MarsRover.EnvironmentHat")
        
        self.weatherSensor = BME280(bus=i2c_bus)
        self.lightSensor = TSL2591(bus=i2c_bus)
        self.uvSensor = LTR390(bus=i2c_bus)
        # self.vocSensor = SGP40(i2c_bus)
        self.motionSensor = ICM20948(bus=i2c_bus)
        self.distance_sensor = DistanceSensor()

        
        self.distance_measure_stopped: bool = True

    def get_lux(self) -> float:
        return self.lightSensor.get_lux()

    def get_temperature(self) -> float:
        return self.weatherSensor.getTemperature()

    def get_pressure(self) -> float:
        return self.weatherSensor.getPressure()

    def get_humidity(self) -> float:
        return self.weatherSensor.getHumidity()

    def get_uv(self) -> float:
        return self.uvSensor.getUV()
    
    # def get_voc(self) -> int:
    #     temp = int(round(self.get_temperature(), 0))
    #     hum = int(round(self.get_humidity(), 0))
    #     # self.vocSensor.get_voc_index(temp, hum)
    #     return 100

    #TODO: implement motion sensing

    def get_distance_front(self) -> float:
        return self.distance_sensor.get_distance()

    def start_distance_measure(self) -> Thread:
        self.logger.debug("start distance measure")
        if self.distance_measure_stopped == True:
            self.distance_measure_stopped = False
            distance_measurement_thread = Thread(target=self.continuous_distance_measure, name="DistanceMeasurement")
            distance_measurement_thread.start()
            return distance_measurement_thread
        else:
            self.logger.warning("distance measure already running")
            return None

    def stop_distance_measure(self):
        self.logger.debug("stopp distance measure")
        self.distance_measure_stopped = True
        MarsRover.distance_front = 0
        
    def continuous_distance_measure(self):
        while True:
            if self.distance_measure_stopped:
                break
            MarsRover.distance_front = self.get_distance_front()
        
    def get_meteo_light_measures(self, round_measure_by: int = None) -> dict:
        temp = self.get_temperature()
        hum = self.get_humidity()
        press = self.get_pressure()
        uv = self.get_uv()
        lux = self.get_lux()
        # voc = self.get_voc()
        measures_dict = {
            "temperature": temp,
            "humidity": hum,
            "pressure": press,
            "uv": uv,
            "light": lux
        }
        if round_measure_by >= 0:
            for key, value in measures_dict.items():
                try:
                    measures_dict[key] = round(value, round_measure_by)
                except:
                    self.logger.warning(f"failed to round {key}: {value}")
        return measures_dict