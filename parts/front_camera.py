from time import sleep
from picamera import PiCamera
from datetime import datetime
from servocontroller import ServoController
import logging

class FrontCamera:
    MOVE_TIME = 0.3

    def __init__(self, camera_enabled: bool, servoController: ServoController) -> None:
        self.logger = logging.getLogger(f"MarsRover.FrontCamera")
        self.cs1 = servoController.CS1
        self.camera_enabled = camera_enabled
        if self.camera_enabled:
            self.camera = PiCamera(camera_num=0, resolution=(2560, 1440))
            self.camera.rotation = 180

    def takePicture(self):
        if self.check_camera():
            timestamp = str(datetime.now().strftime("%d-%m-%Y_%H:%M:%S:%f"))
            picturePath = f"Pictures/{timestamp}_FrontCamera.jpg"
            self.logger.info(f"take picture: '{picturePath}'")
            self.camera.start_preview()
            self.camera.capture(picturePath)
            sleep(0.1)

    def dispatchservo(self):
        self.cs1.dispatch()

    def point(self, degree: int):
        self.logger.info(f"point to {degree} degrees")
        if degree == 0:
            self.cs1.toMin()
        elif degree == 45:
            self.cs1.toLMid()
        elif degree == 90:
            self.cs1.toMid()
        elif degree == 135:
            self.cs1.toRMid()
        elif degree == 180:
            self.cs1.toMax()
        sleep(self.MOVE_TIME)

    def takePanorama(self):
        if self.check_camera():
            self.logger.info("take panorama of containing 5 pictures")
            # begin LEFT at 0 degrees
            self.point(180)
            self.takePicture()
            self.point(135)
            self.takePicture()
            self.point(90)
            self.takePicture()
            self.point(45)
            self.takePicture()
            self.point(0)
            self.takePicture()
            # back to center
            self.point(90)

    def check_camera(self):
        if self.camera_enabled:
            return True
        else:
            self.logger.error("camera disabled")
            return False