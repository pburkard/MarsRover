import sys
sys.path.append("/home/pi/MarsRover/web")
sys.path.append("/home/pi/MarsRover/marsrovercore")
from web import app, rover
from marsrovercore.enums import StartMode
import marsrovercore.logginghelper as logginghelper
import logging

logger: logging.Logger = None

if(__name__ == '__main__'):
    try:
        logger_root = logginghelper.create_logger("MarsRover", logging.INFO)
        logger = logging.getLogger(f"MarsRover.{StartMode.WEBCONTROL.name}")
        rover.take_default_position()
        # run flask app
        app.run(host='0.0.0.0', port=8181)
    except KeyboardInterrupt:
        rover.logger.critical("exit triggered by KEYBOARDINTERRUPT")
    except Exception as ex:
        rover.logger.critical("exit triggered by EXCEPTION")
        rover.logger.exception(ex)
    finally:
        if rover:
            rover.pull_handbreak()
            rover.gpio.cleanup_all()
        if logger:
            rover.logger.critical('END \n------------------------------------------------------------------')

