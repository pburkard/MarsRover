import sys
sys.path.append("/home/pi/MarsRover/marsrovercore")

from marsrovercore.enums import WheelPosition, DriveDirection, StartMode
from marsrovercore.marsrover import MarsRover
from time import sleep

rover: MarsRover

def drivetest():
    rover.takeDefaultPosition()
    rover.drive_direction = DriveDirection.FORWARD
    rover.start_drive(duration=2)
    rover.setwheelposition(WheelPosition.CIRCULAR)
    rover.start_drive(duration=1)

def sensortest():
    print(rover.sensorcontroller.get_meteo_light_measures(round_measure_by=4))

def wheelpositiontest():
    rover.takeDefaultPosition()
    for position in WheelPosition:
        rover.setwheelposition(position)
        sleep(0.5)
    rover.takeDefaultPosition()

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
    rover.start_distance_measure()

def drive_square_test(timePerSide):
    rover.takeDefaultPosition()
    rover.drive_speed = 0.6
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
    # vertical/circular
    for _ in range(4):
        rover.setwheelposition(WheelPosition.VERTICAL)
        rover.drive_direction = DriveDirection.FORWARD
        rover.start_drive(duration=timePerSide)
        rover.drive_direction = DriveDirection.TURN_LEFT
        rover.turn(90)

if(__name__ == '__main__'):
    rover = MarsRover(camera_enabled=False)

    rover.logger.critical('START')
    rover.logger.critical(f'mode: {StartMode.TESTBED.name}')

    try:
        rover.keep_distance_start()
    except KeyboardInterrupt:
        rover.logger.critical("exit triggered by KEYBOARDINTERRUPT")
        rover.pull_handbreak()
    except Exception as ex:
        rover.logger.critical("exit triggered by EXCEPTION")
        rover.logger.exception(ex)
    finally:
        rover.gpio.cleanup_all()
    rover.logger.critical('END \n------------------------------------------------------------------')