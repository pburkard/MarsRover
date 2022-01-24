import marsrover
from time import sleep

rover: marsrover.MarsRover

if(__name__ == '__main__'):
    rover = marsrover.MarsRover(camera_enabled=True)
    rover.logger.critical('START')
    rover.logger.critical(f'mode: {marsrover.StartMode.AUTONOMOUS.name}')

    try:
        rover.takeDefaultPosition()
        
    except KeyboardInterrupt:
        rover.handbreak = True
        sleep(1)
    finally:
        rover.cleanup()
    
    rover.logger.critical('END \n------------------------------------------------------------------')