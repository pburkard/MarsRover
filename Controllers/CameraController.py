import time
from picamera import PiCamera
from datetime import datetime
from os.path import exists
import Controllers.ServoController as ServoController
import logging

from Classes.HD1370A import HD1370A

logger = logging.getLogger('MarsRover.CameraController')

camera = PiCamera(camera_num=0, resolution=(2560, 1440))
camera.rotation = 180

def takePicture():
    timestamp = str(datetime.now().strftime("_%d-%m-%Y_%H:%M:%S:%f"))
    picturePath = f"Pictures/maincam{timestamp}.jpg"
    logger.debug(f"picture path: {picturePath}")
    camera.start_preview()
    camera.capture(picturePath)
    logger.debug(f"picture taken")

def pointTo(direction):
    pulse = 0

    if(direction == 1):
        pulse = HD1370A.Min
    if(direction == 2):
        pulse = HD1370A.RMid
    if(direction == 3):
        pulse = HD1370A.Mid
    if(direction == 4):
        pulse = HD1370A.LMid
    if(direction == 5):
        pulse = HD1370A.Max
    
    ServoController.moveHD1370A(pulse)
    time.sleep(0.25)
    ServoController.dispatchCamServo()