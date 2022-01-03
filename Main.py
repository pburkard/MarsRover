from Classes.ServoController import ServoController
from Classes.MotorController import MotorController
from Classes.RaspberryPi import RaspberryPi
from Classes.FrontCamera import FrontCamera
from Classes.DistanceSensor import DistanceSensor
from Classes.EnvironmentHat import EnvironmentHat
import logging
import datetime
import os
from Adafruit_PCA9685 import PCA9685
from time import sleep
from Enums import WheelPosition, DriveDirection
from threading import Thread

pca9685 = PCA9685()
pca9685.set_pwm_freq(60)
rpi = RaspberryPi()
servoController = ServoController(pca9685)
motorController = MotorController(pca9685, rpi)
frontCamera = FrontCamera(servoController)
distanceSensor = DistanceSensor(rpi)
envHat = EnvironmentHat()

measuredDistance: float = 0.0
runMeasurement: bool = True
motorsEnabled: bool = False
direction: DriveDirection = DriveDirection.FORWARD
handbreak: bool = False

def main():
    logger.critical('START')
    global handbreak
    try:
        takeDefaultPosition()
        # startDistanceMeasurement()
        # keepDistanceToObject()
        
    except KeyboardInterrupt:
        handbreak = True
        sleep(1)
    finally:
        rpi.gpioCleanup()
        logger.critical('END \n------------------------------------------------------------------')

def createLogger(levelConsole) -> logging.Logger:
    logger = logging.getLogger("MarsRover")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s")
    # console logging
    ch = logging.StreamHandler()
    ch.setLevel(levelConsole)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # file logging
    currentDirectory = os.getcwd()
    fileName = f"MarsRover_{datetime.date.today().strftime('%d-%m-%Y')}.log"
    file = rf"{currentDirectory}/Logfiles/{fileName}"
    print(file)
    try:
        fh = logging.FileHandler(file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception:
        logger.error("failed to add filehandler")
    return logger

def servoTest():
    logger.critical("start")
    servoController.rotateWheelsHorizontal()
    sleep(1)
    servoController.rotateWheelsVertical()
    sleep(1)
    servoController.dispatchDriveServos()

def rectangleDriveTest(timePerSide, speed):
    logger.critical("start")
    servoController.rotateWheelsVertical()
    motorController.drive(timePerSide, speed, WheelPosition.VERTICAL)

    servoController.rotateWheelsHorizontal()
    motorController.drive(timePerSide, speed, WheelPosition.HORIZONTAL)

    servoController.rotateWheelsVertical()
    motorController.drive(timePerSide, -speed, WheelPosition.VERTICAL)

    servoController.rotateWheelsHorizontal()
    motorController.drive(timePerSide, -speed, WheelPosition.HORIZONTAL)
    
    servoController.rotateWheelsVertical()

def emergencyHandbreak():
    global measuredDistance
    while True:
        if measuredDistance < 20:
            pullHandbreak()
            break
    logger.critical("end")

def pullHandbreak():
    logger.critical("pull handbreak")
    global handbreak
    handbreak = True

def startDistanceMeasurement():
    threadDistanceMeasurement = Thread(target=distanceMeasurement, args=())
    threadDistanceMeasurement.start()

def distanceMeasurement():
    global measuredDistance
    global runMeasurement
    while runMeasurement:
        if(handbreak):
            break
        measuredDistance = distanceSensor.getDistance()
        sleep(0.1)
    logger.critical("end")

def verticalDriveTest():
    logger.critical("start")
    servoController.rotateWheelsVertical()
    motorController.drive(1, 0.8, WheelPosition.VERTICAL)
    sleep(1)
    motorController.drive(1, -0.8, WheelPosition.VERTICAL)

def keepDistanceToObject():
    threadDriveCoordinator = Thread(target=coordinateDistanceToObject, args=(35.0, 40.0))
    threadDrive = Thread(target=driveInDistanceToObject)
    threadDriveCoordinator.start()
    threadDrive.start()
    threadDriveCoordinator.join()
    threadDrive.join()

def driveInDistanceToObject():
    logger.critical("start")
    global motorsEnabled
    global direction
    global handbreak

    servoController.rotateWheelsVertical()
    while True:
        if handbreak:
            break
        if motorsEnabled:
            speed = 0.2
            if direction == DriveDirection.REVERSE:
                speed = speed*(-1)
            motorController.drive(0.5, speed, WheelPosition.VERTICAL)

def coordinateDistanceToObject(preferredDistanceMin: float, preferredDistanceMax: float):
    logger.critical("start")
    global measuredDistance
    global motorsEnabled
    global direction
    global handbreak
    while not handbreak:
        if(preferredDistanceMax < measuredDistance):
            logger.debug("too far from object")
            # drive forward
            direction = DriveDirection.FORWARD
            motorsEnabled = True
        elif(preferredDistanceMin > measuredDistance):
            logger.debug("too close to object")
            # drive reverse
            direction = DriveDirection.REVERSE
            motorsEnabled = True
        elif(preferredDistanceMin <= measuredDistance and preferredDistanceMax >= measuredDistance):
            logger.debug("in preferred distance to object")
            # stop drive
            motorsEnabled = False
        else:
            logger.debug(f"measured distance: {measuredDistance}, preferred distance between min: {preferredDistanceMin} and max: {preferredDistanceMax}")
            raise Exception("VERY wrong")
        sleep(0.1)
    logger.critical("end")

def takeDefaultPosition():
    logger.critical("start")
    servoController.rotateWheelsVertical()
    frontCamera.point90()

def horizontalDriveTest():
    logger.critical("start")
    servoController.rotateWheelsHorizontal()
    motorController.drive(1, 0.8, WheelPosition.HORIZONTAL)
    sleep(1)
    motorController.drive(1, -0.8, WheelPosition.HORIZONTAL)

if(__name__ == '__main__'):
    logger = createLogger(levelConsole=logging.DEBUG)
    main()