import Controllers.MotorController as MotorController
import Controllers.ServoController as ServoController
import Controllers.CameraController as CameraController
import Controllers.EnvironmentController as EnvironmentController
import RPi.GPIO as io
import time
import logging
from Classes.RaspberryPi import RaspberryPi

logger = logging.getLogger('MarsRover.RPiController')

rpi = RaspberryPi()

IN1 = rpi.pin6
IN2 = rpi.pin13
IN3 = rpi.pin19
IN4 = rpi.pin26

def testServos():
    try:
        logger.info('start testServos')

        ServoController.leftToMin()
        ServoController.rightToMin()
        time.sleep(1)
        ServoController.leftToMax()
        ServoController.rightToMax()
        time.sleep(1)
        ServoController.allToCenter()
        time.sleep(1)

        ServoController.dispatchServos()
    except Exception as e:
        logger.exception(f"exception thrown: {e}")
    finally:
        endOfDrive()

def testDrive():
    try:
        logger.info("start test drive")
        ServoController.allToCenter()
        time.sleep(1)
        driveForward(2, 0.8)
        time.sleep(1)
        driveReverse(2, 0.8)
    except Exception as e:
        logger.info(f"exception thrown: {e}")
    finally:
        endOfDrive()

def testPicture():
    CameraController.pointTo(1)
    time.sleep(0.5)
    CameraController.pointTo(2)
    time.sleep(0.5)
    CameraController.pointTo(3)
    time.sleep(0.5)
    CameraController.pointTo(4)
    time.sleep(0.5)
    CameraController.pointTo(5)
    time.sleep(0.5)
    # CameraController.takePicture()

def takePictures():
    CameraController.pointTo(3)
    CameraController.takePicture()
    CameraController.pointTo(4)
    CameraController.takePicture()
    CameraController.pointTo(5)
    CameraController.takePicture()
    CameraController.pointTo(1)
    CameraController.takePicture()
    CameraController.pointTo(2)
    CameraController.takePicture()
    # move back to center
    CameraController.pointTo(3)

def driveForward(duration, speed):
    logger.info(f'start {driveForward.__name__}')
    io.output(IN1, io.HIGH)
    io.output(IN3, io.HIGH)

    MotorController.setFrontMotors(speed)
    MotorController.setRearMotors(speed)

    time.sleep(duration)

    io.output(IN1, io.LOW)
    io.output(IN3, io.LOW)

def driveReverse(duration, speed):
    logger.info(f'start {driveReverse.__name__}')
    io.output(IN2, io.HIGH)
    io.output(IN4, io.HIGH)

    MotorController.setFrontMotors(speed)
    MotorController.setRearMotors(speed)

    time.sleep(duration)

    io.output(IN2, io.LOW)
    io.output(IN4, io.LOW)

def takeEnvironmentMeasurement():
    EnvironmentController.getTemperature()
    EnvironmentController.getPressure()
    EnvironmentController.getHumidity()
    EnvironmentController.getUV()
    EnvironmentController.getGas()

    

def endOfDrive():
    logger.info(f'start {endOfDrive.__name__}')
    MotorController.dispatchMotors()
    ServoController.dispatchServos()

