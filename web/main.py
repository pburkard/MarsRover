from web import app, rover, logger

try:
    logger.critical('START WEB')
    rover.drive_speed = 0.6
    rover.take_default_position()
    # run flask app
    app.run(host='0.0.0.0', port=8181)
except KeyboardInterrupt:
    logger.critical("exit triggered by KEYBOARDINTERRUPT")
except Exception as ex:
    logger.critical("exit triggered by EXCEPTION:")
    logger.exception(ex)
finally:
    if rover:
        rover.pull_handbreak()
        rover.gpio.cleanup_all()
    logger.critical('END WEB\n------------------------------------------------------------------')