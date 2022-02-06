import sys
sys.path.append("/home/pi/MarsRover/web")
sys.path.append("/home/pi/MarsRover/marsrovercore")

from time import sleep
from web import app, rover
from marsrovercore.enums import StartMode

if(__name__ == '__main__'):
    rover.logger.critical('START')
    rover.logger.critical(f'mode: {StartMode.WEBCONTROL.name}')
    try:
        rover.take_default_position()
        # run flask app
        app.run(host='0.0.0.0', port=8181)
    except KeyboardInterrupt:
        rover.logger.critical("exit triggered by KEYBOARDINTERRUPT")
    except Exception as ex:
        rover.logger.critical("exit triggered by EXCEPTION")
        rover.logger.exception(ex)
    finally:
        rover.pull_handbreak()
        rover.gpio.cleanup_all()
    rover.logger.critical('END \n------------------------------------------------------------------')

