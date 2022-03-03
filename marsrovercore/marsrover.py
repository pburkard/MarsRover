import os
from time import sleep
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from threading import Thread
from marsrovercore.enums import DriveDirection, WheelPosition
import marsrovercore.logginghelper as logginghelper

class MarsRover():
    DEFAULT_SPEED = 0.5
    DEFAULT_DRIVE_DIRECTION = DriveDirection.FORWARD
    DEFAULT_WHEEL_POSITION = WheelPosition.VERTICAL
    SECS_UNTIL_360_TURN: float = 4.5
    MIN_DISTANCE_TO_OBJECT: float = 80

    current_speed: float = 0.0
    drive_speed: float = DEFAULT_SPEED
    drive_direction: DriveDirection = DEFAULT_DRIVE_DIRECTION
    wheel_position: WheelPosition = DEFAULT_WHEEL_POSITION

    def __init__(self, camera_enabled: bool):
        from modules.gpio import GPIO
        from controllers.servocontroller import ServoController
        from controllers.motorcontroller import MotorController
        from marsrovercore.modules.camera import Camera
        from controllers.sensorcontroller import SensorController

        self.logger = logginghelper.get_logger("Core")
        self.gpio = GPIO()
        self.circuitpython_i2c_bus1 = busio.I2C(SCL, SDA)
        self.pca9685 = PCA9685(self.circuitpython_i2c_bus1, address=65)
        self.pca9685.frequency = 60
        self.servocontroller = ServoController(self.pca9685)
        self.motorcontroller = MotorController(self.gpio, self.pca9685)
        self.sensorcontroller = SensorController(i2c_bus_number=3)
        self.front_camera = Camera(camera_enabled, self.servocontroller)
        
        self.distance_measure_thread: Thread = None
        self.measurement_out_of_range: bool = True
        self.keep_distance_stopped: bool = True
        self.keep_distance_coordinate_thread: Thread = None
        self.keep_distance_drive_thread: Thread = None

        # set default wheel position
        self.servocontroller.set_drive_servos(self.DEFAULT_WHEEL_POSITION)
        self.front_camera.point(90)

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
        
    def keep_distance_drive(self):
        self.take_default_position()
        while True:
            if self.keep_distance_stopped:
                self.stop_drive()
                break
            if self.measurement_out_of_range:
                if self.wheel_position == WheelPosition.VERTICAL:
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
                self.measurement_out_of_range = True
            elif(preferredDistanceMin > distance_front):
                self.logger.debug("too close to object")
                # drive reverse
                self.drive_direction = DriveDirection.REVERSE
                self.measurement_out_of_range = True
            elif(preferredDistanceMin <= distance_front and preferredDistanceMax >= distance_front):
                self.logger.debug("in preferred distance to object")
                # stop drive
                self.measurement_out_of_range = False
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
            sleep(0.2)
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
                self.logger.info(f"start drive with speed: {self.current_speed} for {duration}secs")
                sleep(duration)
                self.stop_drive()
            else:
                self.logger.info(f"start drive with speed: {self.current_speed}")

    def stop_drive(self):
        if self.current_speed > 0:
            self.motorcontroller.dispatch_all()
            self.current_speed = 0
    
    def drive_until_distance_is(self, preferred_distance: float):
        buffer_preferred_distance = preferred_distance + 5
        if self.sensorcontroller.distance_front > buffer_preferred_distance:
            self.logger.info(f"stop drive when approx. {preferred_distance}mm away")
            drive_speed_temp = self.drive_speed 
            while self.sensorcontroller.distance_front > buffer_preferred_distance:
                current_distance = self.sensorcontroller.distance_front
                close = buffer_preferred_distance + 100
                closeup_speed = 0.15
                if current_distance <= close and self.current_speed > closeup_speed:
                    self.logger.info(f"close up to object: {current_distance}")
                    self.stop_drive()
                    self.drive_speed = closeup_speed
                    self.start_drive()
                sleep(0.05)
            self.stop_drive()
            self.logger.info(f"distance at stop: {self.sensorcontroller.distance_front}")
            self.drive_speed = drive_speed_temp   

    def turn(self, to_angle: int):
        self.logger.info(f"start turn to {to_angle}°")
        self.setwheelposition(WheelPosition.CIRCULAR)
        temp_speed = self.drive_speed
        self.drive_speed = 1
        secs = self.SECS_UNTIL_360_TURN / 360 * to_angle
        self.start_drive(duration=secs)
        self.drive_speed = temp_speed

    def take_panorama(self):
        if self.check_camera():
            self.logger.info("take panorama of containing 5 pictures")
            angles = [180, 135, 90, 45, 0]
            for angle in angles:
                self.point(angle)
                self.take_picture()
            # back to center
            self.point(90)

    def shutdown():
        os.system("sudo halt &")

    def reboot():
        os.system("sudo reboot &")