import adafruit_vl53l0x
import board
import busio
import logging
from time import sleep
from parts.raspberrypi import RaspberryPi

class DistanceSensor:
    def __init__(self, rpi: RaspberryPi):
        self.logger = logging.getLogger("MarsRover.DistanceSensor")

        self.rpi = rpi
        self.rpi.setGPIO(self.rpi.TOF_XSHUT, self.rpi.OUT, self.rpi.HIGH)

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
        self.sensor.measurement_timing_budget = 200000

    def getDistance(self):
        distance = self.sensor.distance
        self.logger.info(f"distance measure: {distance}")
        return distance


# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
#vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.
