from time import sleep
from picamera import PiCamera
from datetime import datetime
from controllers.servocontroller import ServoController
import marsrovercore.logginghelper as logginghelper

class Camera:
    def __init__(self, camera_enabled: bool) -> None:
        self.name = 'C1'
        self.logger = logginghelper.get_logger(f"Camera.{self.name}")
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

    def check_camera(self):
        if self.camera_enabled:
            return True
        else:
            self.logger.error("camera disabled")
            return False