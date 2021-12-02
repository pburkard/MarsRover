import Controllers.RPiController as RPiController
import logging
import datetime
from Classes.RaspberryPi import RaspberryPi

logger = logging.getLogger('MarsRover')
logger.setLevel(logging.DEBUG)

fileName = f"marsrover_{datetime.date.today().strftime('%d-%m-%Y')}.log"
file = rf"/home/pi/rover/Logfiles/{fileName}"
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# file logging
fh = logging.FileHandler(file)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# console logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch) 

logger.debug('start main')

rpi = RaspberryPi()

# RPiController.testServos()
# RPiController.testDrive()
# RPiController.takePictures()
RPiController.takeEnvironmentMeasurement()

rpi.gpioCleanup()

logger.debug('end of program')
