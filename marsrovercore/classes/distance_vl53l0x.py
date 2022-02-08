from threading import Thread
import adafruit_vl53l0x
import board
import busio
import logging

class DistanceSensor:
    def __init__(self):
        self.logger = logging.getLogger("MarsRover.DistanceSensor")
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
        self.sensor.measurement_timing_budget = 50000

    def get_distance(self):
        measure_in_mm = self.sensor.range
        calibration_in_mm = 90
        distance = measure_in_mm - calibration_in_mm
        self.logger.debug(f"distance measure: {distance}mm")
        return distance


# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
#vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.
