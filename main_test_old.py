import sys
from threading import Thread
sys.path.append("/home/pi/MarsRover/marsrovercore")
from marsrovercore.enums import WheelPosition, DriveDirection, StartMode
from marsrovercore.marsrover import MarsRover
import marsrovercore.logginghelper as logginghelper
from time import sleep
import logging

logger: logging.Logger = None
rover: MarsRover = None

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

def drive_parkour_1():
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

if(__name__ == '__main__'):
    try:
        logger_root = logginghelper.create_logger("MarsRover", logging.INFO)
        logger = logging.getLogger(f"MarsRover.{StartMode.TESTBED.name}")
        rover = MarsRover(camera_enabled=False)
        # camera_enabled has to be FALSE currently. This is due to the MJPG STREAMER for main_web's live video feed.
        # It would be possible to use grab a frame from port 8080 like the web module does for its video feed
        logger.critical('START')
    except KeyboardInterrupt:
        logger.critical("exit triggered by KEYBOARDINTERRUPT")
    except Exception as ex:
        logger.critical("exit triggered by EXCEPTION")
        logger.exception(ex)
    finally:
        if rover:
            rover.pull_handbreak()
            rover.gpio.cleanup_all()
        if logger:
            logger.critical('END \n------------------------------------------------------------------')