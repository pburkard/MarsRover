import sys
sys.path.append("/home/pi/MarsRover/marsrovercore")

from marsrovercore.enums import WheelPosition, DriveDirection, StartMode
from marsrovercore.marsrover import MarsRover
from time import sleep

rover: MarsRover

def drivetest():
    rover.takeDefaultPosition()
    rover.driveDirection = DriveDirection.FORWARD
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

def horizontalPositionCalibration():
    rover.setwheelposition(WheelPosition.HORIZONTAL)
    sleep(0.5)

if(__name__ == '__main__'):
    rover = MarsRover(camera_enabled=False)

    rover.logger.critical('START')
    rover.logger.critical(f'mode: {StartMode.TESTBED.name}')

    try:
        horizontalPositionCalibration()
    except KeyboardInterrupt:
        rover.logger.critical("exit triggered by KEYBOARDINTERRUPT")
        rover.pullHandbreak()
        sleep(1)
    except Exception as ex:
        rover.logger.critical("exit triggered by EXCEPTION")
        rover.logger.exception(ex)
    finally:
        rover.cleanup()
    
    rover.logger.critical('END \n------------------------------------------------------------------')