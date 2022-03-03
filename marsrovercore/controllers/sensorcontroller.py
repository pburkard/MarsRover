import logging
from time import sleep
from modules.light_tsl2591 import TSL2591
# from modules.voc_sgp40_2 import SGP40
from modules.uv_ltr390 import LTR390
from modules.motion_icm20948 import ICM20948
from modules.weather_bme280 import BME280
from modules.distance_vl53l0x import DistanceSensor

class SensorController():
    def __init__(self, i2c_bus_number: int) -> None:
        self.logger = logging.getLogger("MarsRover.EnvironmentHat")
        
        self.weatherSensor = BME280(bus=i2c_bus_number)
        self.lightSensor = TSL2591(bus=i2c_bus_number)
        self.uvSensor = LTR390(bus=i2c_bus_number)
        # self.vocSensor = SGP40(i2c_bus)
        # self.motionSensor = ICM20948(bus=i2c_bus)
        self.distance_sensor = DistanceSensor()

        self.distance_front: float = 0.0
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
    
    def get_motion_measures(self):
        data = self.motionSensor.getdata()
        motion_dict = {
            "roll": data[0],
            "pitch": data[1],
            "yaw": data[2],
            "accel_x": data[3],
            "accel_y": data[4],
            "accel_z": data[5],
            "gyro_x": data[6],
            "gyro_y": data[7],
            "gyro_z": data[8],
            "mag_x": data[9],
            "mag_y": data[10],
            "mag_z": data[11]
        }
        self.logger.info(motion_dict)
        return motion_dict

    def get_distance_front(self) -> float:
        return self.distance_sensor.get_distance()
        
    def continuous_distance_measure(self):
        while True:
            if self.distance_measure_stopped:
                break
            self.distance_front = self.get_distance_front()
            # sleep(0.1)
        
    def get_meteo_light_measures(self, round_measure_by: int = -1) -> dict:
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