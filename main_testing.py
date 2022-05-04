import sys
sys.path.append("/home/pi/MarsRover/marsrovercore")
from marsrovercore.enums import WheelPosition, DriveDirection
from marsrovercore.marsrover import MarsRover
from time import sleep
import logging
import os
import datetime

def drivetest():
    rover.drive_direction = DriveDirection.FORWARD
    rover.drive_speed = 1
    rover.start_drive(duration=2)

def sensortest():
    print(rover.sensorcontroller.get_meteo_light_measures(round_measure_by=4))

def wheelpositiontest():
    for position in WheelPosition:
        rover.setwheelposition(position)
        sleep(0.5)

def calibrate_horizontal_position():
    rover.setwheelposition(WheelPosition.HORIZONTAL)
    sleep(0.5)

def calibrate_circular_turn():
    # how much drive-seconds are 360°?
    # value in full speed
    rover.setwheelposition(WheelPosition.CIRCULAR)
    rover.drive_speed = 1
    rover.start_drive(duration=5.25)

def calibrate_distance_vl53l0x():
    rover.sensorcontroller.distance_measure_start()

def drive_square_test_horizontal(timePerSide):
    rover.take_default_position()
    rover.drive_speed = 0.8
    # vertical/horizontal
    rover.drive_direction = DriveDirection.FORWARD
    rover.start_drive(duration=timePerSide)
    rover.setwheelposition(WheelPosition.HORIZONTAL)
    rover.drive_direction = DriveDirection.REVERSE
    rover.start_drive(duration=timePerSide)
    rover.setwheelposition(WheelPosition.VERTICAL)
    rover.drive_direction = DriveDirection.REVERSE
    rover.start_drive(duration=timePerSide)
    rover.setwheelposition(WheelPosition.HORIZONTAL)
    rover.drive_direction = DriveDirection.FORWARD
    rover.start_drive(duration=timePerSide)

def drive_square_test_circular(timePerSide):
    rover.take_default_position()
    rover.drive_speed = 0.8
    # vertical/circular
    for _ in range(4):
        rover.setwheelposition(WheelPosition.VERTICAL)
        rover.drive_direction = DriveDirection.FORWARD
        rover.start_drive(duration=timePerSide)
        rover.drive_direction = DriveDirection.TURN_LEFT
        rover.turn(90)

def picturetest():
    rover.front_camera.point(45)
    rover.front_camera.take_picture()

def show_off():
    rover.drive_direction = DriveDirection.REVERSE
    rover.drive_speed = 0.4
    rover.start_drive(duration=2)
    rover.setwheelposition(WheelPosition.CIRCULAR)
    rover.drive_direction = DriveDirection.TURN_RIGHT
    rover.turn(90)
    rover.setwheelposition(WheelPosition.VERTICAL)
    sleep(0.5)
    rover.front_camera.point(45)
    sleep(0.5)
    rover.front_camera.point(135)
    sleep(0.5)
    rover.front_camera.point(90)

def drive_course_1():
    rover.distance_measure_start()
    rover.drive_speed = 0.8
    rover.start_drive()
    rover.drive_until_distance_is(100)
    rover.front_camera.point(0)
    sleep(1)
    rover.front_camera.point(90)
    rover.turn(90)
    rover.setwheelposition(WheelPosition.VERTICAL)
    rover.start_drive()
    rover.drive_until_distance_is(100)
    rover.drive_direction = DriveDirection.TURN_RIGHT
    rover.front_camera.point(180)
    sleep(1)
    rover.front_camera.point(90)
    rover.turn(90)
    rover.drive_direction = DriveDirection.FORWARD
    rover.setwheelposition(WheelPosition.VERTICAL)
    rover.start_drive(duration=1.5)

# voc sensor on the environment hat seems to be dead. i2cdetect -y 3 does not find 0x59 VOC
# def voc_sensor_test():
#     rover.sensorcontroller.get_voc()

# create root logger
root_logger = logging.getLogger("Root-Test")
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s")
# console logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
root_logger.addHandler(ch)
# file logging
filelogger_dir_name = "logfiles"
current_dir = os.getcwd()
filelogger_dir = rf"{current_dir}/{filelogger_dir_name}"
if not os.path.isdir(filelogger_dir):
    os.mkdir(filelogger_dir)
logfile_name = f"MarsRover_{datetime.date.today().strftime('%d-%m-%Y')}.log"
logfile_path = rf"{filelogger_dir}/{logfile_name}"
fh = logging.FileHandler(logfile_path)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
root_logger.addHandler(fh)

root_logger.critical('START')
rover: MarsRover = None
try:
    rover = MarsRover(camera_enabled=False)
    # camera_enabled has to be FALSE currently. This is due to the MJPG STREAMER for main_web's live video feed.
    # It would be possible to use grab a frame from port 8080 like the web module does for its video feed
    wheelpositiontest()
except KeyboardInterrupt:
    root_logger.critical("exit triggered by KEYBOARDINTERRUPT")
except Exception as ex:
    root_logger.critical("exit triggered by EXCEPTION")
    root_logger.exception(ex)
finally:
    if rover:
        rover.pull_handbreak()
        rover.gpio.cleanup_all()
    root_logger.critical('END \n------------------------------------------------------------------')
