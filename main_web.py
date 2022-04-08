

from marsrovercore.enums import StartMode
import marsrovercore.logginghelper as logginghelper
import logger



if(__name__ == '__main__'):
    logger_root = logginghelper.create_logger("MarsRover", logging.INFO)
    logger = logging.getLogger(f"MarsRover.{StartMode.WEBCONTROL.name}")
    try:
        
        from web import app, rover
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

