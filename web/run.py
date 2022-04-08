import sys
sys.path.append("/home/pi/MarsRover")

import ...MarsRover
from web import app
import marsrovercore.logginghelper as logginghelper
import logging
from marsrovercore.enums import StartMode

if(__name__ == '__main__'):
    logger = logging.getLogger(StartMode.WEBCONTROL.name)
    try:
        rover.take_default_position()
        # run flask app
        app.run(host='0.0.0.0', port=8181)
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
            rover.logger.critical('END \n------------------------------------------------------------------')

