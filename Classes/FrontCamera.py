from time import sleep
from picamera import PiCamera
from datetime import datetime
from Classes.ServoController import ServoController
import logging

class FrontCamera:
    MOVE_TIME = 0.3

    def __init__(self, servoController: ServoController) -> None:
        self.logger = logging.getLogger(f"MarsRover.FrontCamera")
        self.servo = servoController.CS1
        self.camera = PiCamera(camera_num=0, resolution=(2560, 1440))
        self.camera.rotation = 180

    def takePicture(self):
        timestamp = str(datetime.now().strftime("%d-%m-%Y_%H:%M:%S:%f"))
        picturePath = f"Pictures/{timestamp}_FrontCamera.jpg"
        self.logger.info(f"take picture: '{picturePath}'")
        self.camera.start_preview()
        self.camera.capture(picturePath)
        # sleep(0.1)


    def point0(self):
        self.logger.info("point to 0 degrees")
        self.servo.toMin()
        sleep(self.MOVE_TIME)

    def point45(self):
        self.logger.info("point to 45 degrees")
        self.servo.toLMid()
        sleep(self.MOVE_TIME)

    def point90(self):
        self.logger.info("point to 90 degrees")
        self.servo.toMid()
        sleep(self.MOVE_TIME)

    def point135(self):
        self.logger.info("point to 135 degrees")
        self.servo.toRMid()
        sleep(self.MOVE_TIME)
        
    def point180(self):
        self.logger.info("point to 180 degrees")
        self.servo.toMax()
        sleep(self.MOVE_TIME)

    def takePanorama(self):
        self.logger.info("take panorama of 5 individual pictures")
        # begin LEFT at 0 degrees
        self.point180()
        self.takePicture()
        self.point135()
        self.takePicture()
        self.point90()
        self.takePicture()
        self.point45()
        self.takePicture()
        self.point0()
        self.takePicture()
        # back to center
        self.point90()