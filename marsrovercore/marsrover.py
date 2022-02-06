import logging
import datetime
import os
from time import sleep
from threading import Thread
from marsrovercore.enums import DriveDirection, WheelPosition

class MarsRover():
    DEFAULT_SPEED = 0.5
    DEFAULT_DRIVE_DIRECTION = DriveDirection.FORWARD
    DEFAULT_WHEEL_POSITION = WheelPosition.VERTICAL
    SECS_UNTIL_360_TURN: float = 5.25

    current_speed: float = 0.0
    drive_speed: float = DEFAULT_SPEED
    drive_direction: DriveDirection = DEFAULT_DRIVE_DIRECTION
    wheel_position: WheelPosition = DEFAULT_WHEEL_POSITION

    def __init__(self, camera_enabled: bool):
        from controllers.servocontroller import ServoController
        from controllers.motorcontroller import MotorController
        from classes.gpio import GPIO
        from classes.front_camera import FrontCamera
        from controllers.sensorcontroller import SensorController
        from Adafruit_PCA9685 import PCA9685

        self.logger = self.create_logger(logging.DEBUG)
        self.pca9685 = PCA9685()
        self.pca9685.set_pwm_freq(60)
        self.gpio = GPIO()
        self.servocontroller = ServoController(self.pca9685)
        self.motorcontroller = MotorController(self.gpio, self.pca9685)
        self.sensorcontroller = SensorController(i2c_bus=3)
        self.front_camera = FrontCamera(camera_enabled, self.servocontroller)
        # set default wheel position
        self.servocontroller.set_drive_servos(self.DEFAULT_WHEEL_POSITION)

        self.keep_distance_stopped: bool = True

    def create_logger(self, levelConsole) -> logging.Logger:
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
            "front_distance": self.sensorcontroller.distance_front,
            "drive_direction": self.drive_direction.name,
            "wheel_position": self.wheel_position.name,
            "camera_position": self.front_camera.current_position
        }
        return status_dict
    
    def pull_handbreak(self):
        self.logger.critical("pull handbreak")
        # stop all threads
        wait_for_threads = False
        if not self.sensorcontroller.distance_measure_stopped:
            wait_for_threads = True
            self.sensorcontroller.distance_measure_stop()
        if not self.keep_distance_stopped:
            wait_for_threads = True
            self.keep_distance_stop()
        if wait_for_threads:
            sleep(1)
        # stop motors and servos
        self.stop_drive()
        self.servocontroller.dispatch_drive_servos()
        self.front_camera.dispatch_servo()
        
    def keep_distance_stop(self):
        if self.keep_distance_stopped == False:
            self.keep_distance_stopped = True
    
    def keep_distance_start(self):
        motors_enabled: bool = True
        def keep_distance():
            self.take_default_position()
            while True:
                if self.keep_distance_stopped:
                    break
                if motors_enabled:
                    self.start_drive()
                else:
                    self.stop_drive()

        def coordinate_distance(preferredDistanceMin: float, preferredDistanceMax: float):
            nonlocal motors_enabled
            while not self.keep_distance_stopped:
                distance_front = self.sensorcontroller.distance_front
                if(preferredDistanceMax < distance_front):
                    self.logger.debug("too far from object")
                    # drive forward
                    self.drive_direction = DriveDirection.FORWARD
                    motors_enabled = True
                elif(preferredDistanceMin > distance_front):
                    self.logger.debug("too close to object")
                    # drive reverse
                    self.drive_direction = DriveDirection.REVERSE
                    motors_enabled = True
                elif(preferredDistanceMin <= distance_front and preferredDistanceMax >= distance_front):
                    self.logger.debug("in preferred distance to object")
                    # stop drive
                    motors_enabled = False
                else:
                    self.logger.debug(f"measured distance: {distance_front}, preferred distance between min: {preferredDistanceMin} and max: {preferredDistanceMax}")
                    raise Exception("VERY wrong")
                sleep(0.2)
        
        if self.keep_distance_stopped == True:
            self.keep_distance_stopped = False
            self.sensorcontroller.distance_measure_start()
            threadDriveCoordinator = Thread(target=coordinate_distance, args=(200.0, 300.0), name="DistanceCoordinator")
            threadDrive = Thread(target=keep_distance, name="DistanceKeeper")
            threadDriveCoordinator.start()
            threadDrive.start()
            threadDriveCoordinator.join()
            threadDrive.join()
        else:
            self.logger.warning("keep distance is already running")

    def take_default_position(self):
        self.setwheelposition(self.DEFAULT_WHEEL_POSITION)
        self.front_camera.point(90)
    
    def setwheelposition(self, position: WheelPosition):
        if not position == self.wheel_position:
            self.servocontroller.set_drive_servos(position)
            self.wheel_position = position

    def start_drive(self, duration: float = 0):
        if self.current_speed == 0:
            self.motorcontroller.setallmotors(self.drive_direction, self.wheel_position, self.drive_speed)
            self.current_speed = self.drive_speed
            
            if duration > 0:
                sleep(duration)
                self.stop_drive()

    def stop_drive(self):
        if self.current_speed > 0:
            self.motorcontroller.dispatch_all()
            self.current_speed = 0
    
    def turn(self, to_angle: int):
        self.setwheelposition(WheelPosition.CIRCULAR)
        temp_speed = self.drive_speed
        self.drive_speed = 1
        secs = self.SECS_UNTIL_360_TURN / 360 * to_angle
        self.start_drive(duration=secs)
        self.drive_speed = temp_speed

    def shutdown():
        os.system("sudo halt &")

    def reboot():
        os.system("sudo reboot &")