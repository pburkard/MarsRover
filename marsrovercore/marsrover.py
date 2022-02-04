import logging
import datetime
import os
from time import sleep
from threading import Thread
from marsrovercore.enums import DriveDirection, WheelPosition

class MarsRover():
    # CONSTANTS & DEFAULTS
    DEFAULT_SPEED = 0.5
    DEFAULT_DRIVE_DIRECTION = DriveDirection.FORWARD
    DEFAULT_WHEEL_POSITION = WheelPosition.VERTICAL

    # Main Properties
    current_speed: float = 0.0
    drive_speed: float = DEFAULT_SPEED
    measuredDistance: float = 0.0
    distancemeasure_running: bool = False
    motorsEnabled: bool = True
    driveDirection: DriveDirection = DEFAULT_DRIVE_DIRECTION
    wheelPosition: WheelPosition = DEFAULT_WHEEL_POSITION
    handbreak: bool = False

    def __init__(self, camera_enabled: bool):
        from controllers.servocontroller import ServoController
        from controllers.motorcontroller import MotorController
        from classes.gpio import GPIO
        from classes.front_camera import FrontCamera
        from controllers.sensorcontroller import SensorController
        from Adafruit_PCA9685 import PCA9685

        self.logger = self.createLogger(logging.DEBUG)
        self.pca9685 = PCA9685()
        self.pca9685.set_pwm_freq(60)
        self.gpio = GPIO()
        self.servocontroller = ServoController(self.pca9685)
        self.motorcontroller = MotorController(self.gpio, self.pca9685)
        self.sensorcontroller = SensorController(i2c_bus=3)
        self.front_camera = FrontCamera(camera_enabled, self.servocontroller)
        # set default wheel position
        self.servocontroller.set_drive_servos(self.DEFAULT_WHEEL_POSITION)

    def createLogger(self, levelConsole) -> logging.Logger:
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
        file = rf"{currentDirectory}/logfiles/{fileName}"
        print(file)
        try:
            fh = logging.FileHandler(file)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception:
            logger.error("failed to add filehandler")
        return logger

    def get_status(self):
        status_dict = {
            "current_speed": self.current_speed,
            "drive_speed": self.drive_speed,
            "frontDistance": self.measuredDistance,
            "driveDirection": self.driveDirection.name,
            "wheelPosition": self.wheelPosition.name,
            "camera_position": self.front_camera.current_position
        }
        return status_dict
    
    # def servoTest(self):
    #     self.logger.critical("start")
    #     self.servocontroller.rotateWheelsHorizontal()
    #     sleep(1)
    #     self.servocontroller.rotateWheelsVertical()
    #     sleep(1)
    #     self.servocontroller.dispatchdriveservos()

    # def rectangleDriveTest(self, timePerSide, speed):
    #     self.logger.critical("start")
    #     self.servocontroller.rotateWheelsVertical()
    #     self.motorcontroller.drive(timePerSide, speed, WheelPosition.VERTICAL)

    #     self.servocontroller.rotateWheelsHorizontal()
    #     self.motorcontroller.drive(timePerSide, speed, WheelPosition.HORIZONTAL)

    #     self.servocontroller.rotateWheelsVertical()
    #     self.motorcontroller.drive(timePerSide, -speed, WheelPosition.VERTICAL)

    #     self.servocontroller.rotateWheelsHorizontal()
    #     self.motorcontroller.drive(timePerSide, -speed, WheelPosition.HORIZONTAL)
        
    #     self.servocontroller.rotateWheelsVertical()

    def emergencyHandbreak(self):
        while True:
            if self.measuredDistance < 20:
                self.pullHandbreak()
                break
        self.logger.critical("end")

    def pullHandbreak(self):
        self.logger.critical("pull handbreak")
        self.handbreak = True

    def start_distance_measure(self):
        self.distancemeasure_running = True
        self.distancemeasure_thread = Thread(target=self.distanceMeasurement, args=())
        self.distancemeasure_thread.start()

    def stop_distance_measure(self):
        self.distancemeasure_running = False
        self.measuredDistance = 0

    def distanceMeasurement(self):
        while True:
            if(self.handbreak or not self.distancemeasure_running):
                break
            self.measuredDistance = self.sensorcontroller.get_distance_front()
            sleep(0.1)
        self.logger.debug("measurement stopped")

    def keepDistanceToObject(self):
        threadDriveCoordinator = Thread(target=self.coordinateDistanceToObject, args=(30.0, 50.0))
        threadDrive = Thread(target=self.driveInDistanceToObject)
        threadDriveCoordinator.start()
        threadDrive.start()
        threadDriveCoordinator.join()
        threadDrive.join()

    # def driveInDistanceToObject(self):
    #     self.logger.critical("start")

    #     self.servocontroller.rotateWheelsVertical()
    #     while True:
    #         if self.handbreak:
    #             break
    #         if self.motorsEnabled:
    #             speed = 0.2
    #             if self.driveDirection == DriveDirection.REVERSE:
    #                 speed = speed*(-1)
    #             self.motorcontroller.drive(0.5, speed, WheelPosition.VERTICAL)

    # def coordinateDistanceToObject(self, preferredDistanceMin: float, preferredDistanceMax: float):
    #     self.logger.critical("start")
    #     while not self.handbreak:
    #         if(preferredDistanceMax < self.measuredDistance):
    #             self.logger.debug("too far from object")
    #             # drive forward
    #             self.driveDirection = DriveDirection.FORWARD
    #             self.motorsEnabled = True
    #         elif(preferredDistanceMin > self.measuredDistance):
    #             self.logger.debug("too close to object")
    #             # drive reverse
    #             self.driveDirection = DriveDirection.REVERSE
    #             self.motorsEnabled = True
    #         elif(preferredDistanceMin <= self.measuredDistance and preferredDistanceMax >= self.measuredDistance):
    #             self.logger.debug("in preferred distance to object")
    #             # stop drive
    #             self.motorsEnabled = False
    #         else:
    #             self.logger.debug(f"measured distance: {self.measuredDistance}, preferred distance between min: {preferredDistanceMin} and max: {preferredDistanceMax}")
    #             raise Exception("VERY wrong")
    #         sleep(0.1)
    #     self.logger.critical("end")

    def takeDefaultPosition(self):
        self.setwheelposition(self.DEFAULT_WHEEL_POSITION)
        self.front_camera.point(90)
    
    def setwheelposition(self, position: WheelPosition):
        if not position == self.wheelPosition:
            self.servocontroller.set_drive_servos(position)
            self.wheelPosition = position

    def start_drive(self, speed: float = 0, duration: float = 0):
        # wheelPosition = self.wheelPosition
        # driveDirection = self.driveDirection

        # if speed == 0:
        #     speed = self.speed
        
        self.motorcontroller.setallmotors(self.driveDirection, self.wheelPosition, self.drive_speed)
        self.current_speed = self.drive_speed
        
        if duration > 0:
            sleep(duration)
            self.stopdrive()

    def stopdrive(self):
        self.motorcontroller.dispatch_all()
        self.current_speed = 0
    
    def cleanup(self):
        self.servocontroller.dispatch_drive_servos()
        self.front_camera.dispatch_servo()
        self.motorcontroller.dispatch_all()
        self.gpio.cleanup_all()

    def shutdown():
        os.system("sudo halt &")

    def reboot():
        os.system("sudo reboot &")