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
        rover.takeDefaultPosition()
        # run flask app
        app.run(host='0.0.0.0', port=8181, debug=False)
    except KeyboardInterrupt:
        rover.pullHandbreak()
        sleep(1)
    except Exception as ex:
        rover.logger.exception(ex)
        rover.pullHandbreak()
        sleep(1)
    finally:
        rover.cleanup()
        rover.logger.critical('END \n------------------------------------------------------------------')

