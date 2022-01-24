import marsrover
from time import sleep

rover: marsrover.MarsRover

def drivetest():
    rover.setwheelposition(marsrover.WheelPosition.VERTICAL)
    rover.driveDirection = marsrover.DriveDirection.FORWARD
    rover.drive(duration=1)

def environment_hat_test():
    print(rover.environment_hat.get_all_measures(round_decimal_place=1))
    for _ in range(2):
        rover.environment_hat.get_voc()
        sleep(1)

def wheelpositiontest():
    rover.setwheelposition(marsrover.WheelPosition.CIRCULAR)
    input()
    rover.setwheelposition(marsrover.WheelPosition.VERTICAL)

if(__name__ == '__main__'):
    rover = marsrover.MarsRover(camera_enabled=False)

    rover.logger.critical('START')
    rover.logger.critical(f'mode: {marsrover.StartMode.TESTBED.name}')

    try:
        # rover.takeDefaultPosition()
        environment_hat_test()

        
    except KeyboardInterrupt:
        rover.pullHandbreak()
        sleep(1)
    finally:
        rover.cleanup()
    
    rover.logger.critical('END \n------------------------------------------------------------------')