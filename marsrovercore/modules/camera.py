from time import sleep
from picamera import PiCamera
from datetime import datetime
from controllers.servocontroller import ServoController
import logging

class Camera:
    MOVE_TIME = 0.3
    current_position: int = None

    def __init__(self, camera_enabled: bool, servoController: ServoController) -> None:
        self.name = 'C1'
        self.logger = logging.getLogger(f"MarsRover.Camera.{self.name}")
        self.cs1 = servoController.CS1
        self.camera_enabled = camera_enabled
        
        if self.camera_enabled:
            self.camera = PiCamera(camera_num=0, resolution=(2560, 1440))
            self.camera.rotation = 180

    def take_picture(self, path: str = 'pictures'):
        if self.check_camera():
            timestamp = str(datetime.now().strftime("%d-%m-%Y_%H:%M:%S:%f"))
            picturePath = f"{path}/{timestamp}_{self.name}.jpg"
            self.logger.info(f"take picture: '{picturePath}'")
            self.camera.start_preview()
            self.camera.capture(picturePath)
            sleep(0.1)

    def dispatch_servo(self):
        self.cs1.dispatch()

    def point(self, degree: int):
        if not degree == self.current_position:
            self.logger.info(f"point to {degree} degrees")
            if degree == 180:
                self.cs1.to_min()
            elif degree == 135:
                self.cs1.to_lmid()
            elif degree == 90:
                self.cs1.to_mid()
            elif degree == 45:
                self.cs1.to_rmid()
            elif degree == 0:
                self.cs1.to_max()
            self.current_position = degree
        sleep(self.MOVE_TIME)

    def take_panorama(self):
        if self.check_camera():
            self.logger.info("take panorama of containing 5 pictures")
            angles = [180, 135, 90, 45, 0]
            for angle in angles:
                self.point(angle)
                self.take_picture()
            # back to center
            self.point(90)

    def check_camera(self):
        if self.camera_enabled:
            return True
        else:
            self.logger.error("camera disabled")
            return False