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
        from classes.gpio import GPIO
        from controllers.servocontroller import ServoController
        from controllers.motorcontroller import MotorController
        from marsrovercore.classes.camera import Camera
        from controllers.sensorcontroller import SensorController
        from Adafruit_PCA9685 import PCA9685

        self.logger = self.create_logger(logging.INFO)
        self.gpio = GPIO()
        self.pca9685 = PCA9685()
        self.pca9685.set_pwm_freq(60)
        self.servocontroller = ServoController(self.pca9685)
        self.motorcontroller = MotorController(self.gpio, self.pca9685)
        self.sensorcontroller = SensorController(i2c_bus=3)
        self.front_camera = Camera(camera_enabled, self.servocontroller)
        
        self.distance_measure_thread: Thread = None
        self.measurment_in_range: bool = True
        self.keep_distance_stopped: bool = True
        self.keep_distance_coordinate_thread: Thread = None
        self.keep_distance_drive_thread: Thread = None

        # set default wheel position
        self.servocontroller.set_drive_servos(self.DEFAULT_WHEEL_POSITION)

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
            fh.setLevel(logging.DEBUG)
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
        self.keep_distance_stop()
        self.distance_measure_stop()
        # stop motors and servos
        self.stop_drive()
        self.servocontroller.dispatch_drive_servos()
        self.front_camera.dispatch_servo()
        
    def keep_distance_drive(self):
        self.take_default_position()
        while True:
            if self.keep_distance_stopped:
                self.stop_drive()
                break
            if self.measurment_in_range:
                self.start_drive()
            else:
                self.stop_drive()

    def keep_distance_coordinate(self, preferredDistanceMin: float, preferredDistanceMax: float):
        while not self.keep_distance_stopped:
            distance_front = self.sensorcontroller.distance_front
            if(preferredDistanceMax < distance_front):
                self.logger.debug("too far from object")
                # drive forward
                self.drive_direction = DriveDirection.FORWARD
                self.measurment_in_range = True
            elif(preferredDistanceMin > distance_front):
                self.logger.debug("too close to object")
                # drive reverse
                self.drive_direction = DriveDirection.REVERSE
                self.measurment_in_range = True
            elif(preferredDistanceMin <= distance_front and preferredDistanceMax >= distance_front):
                self.logger.debug("in preferred distance to object")
                # stop drive
                self.measurment_in_range = False
            else:
                self.logger.debug(f"measured distance: {distance_front}, preferred distance between min: {preferredDistanceMin} and max: {preferredDistanceMax}")
                raise Exception("VERY wrong")
            sleep(0.1)

    def keep_distance_start(self):
        if self.keep_distance_stopped == True:
            self.keep_distance_stopped = False
            self.distance_measure_start()
            sleep(0.1) # wait until first distance measurement is available
            self.keep_distance_coordinate_thread = Thread(target=self.keep_distance_coordinate, args=(200.0, 300.0), name="DistanceCoordinator")
            self.keep_distance_drive_thread = Thread(target=self.keep_distance_drive, name="DistanceKeeper")
            self.keep_distance_coordinate_thread.start()
            self.keep_distance_drive_thread.start()
        else:
            self.logger.warning("keep distance is already running")
    
    def keep_distance_stop(self):
        if not self.keep_distance_stopped:
            self.keep_distance_stopped = True
            self.keep_distance_coordinate_thread.join()
            self.keep_distance_drive_thread.join()

    def distance_measure_start(self):
        if self.sensorcontroller.distance_measure_stopped:
            self.sensorcontroller.distance_measure_stopped = False
            self.distance_measure_thread = Thread(target=self.sensorcontroller.continuous_distance_measure, name="ContinuousDistanceMeasure")
            self.distance_measure_thread.start()
        else:
            self.logger.warning("distance measure already running")

    def distance_measure_stop(self):
        if not self.sensorcontroller.distance_measure_stopped:
            self.sensorcontroller.distance_measure_stopped = True
            self.distance_measure_thread.join()
            self.sensorcontroller.distance_front = 0.0

    def take_default_position(self):
        def take_default_position2():
            self.setwheelposition(self.DEFAULT_WHEEL_POSITION)
            self.front_camera.point(90)
        thread = Thread(target=take_default_position2, name="TakeDefaultPosition")
        thread.start()

    def setwheelposition(self, position: WheelPosition):
        if not position == self.wheel_position:
            self.servocontroller.set_drive_servos(position)
            self.wheel_position = position

    def start_drive(self, duration: float = 0):
        if self.current_speed == 0:
            self.motorcontroller.set_all_motors(self.drive_direction, self.wheel_position, self.drive_speed)
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