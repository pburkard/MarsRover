import sys
sys.path.append("/home/pi/MarsRover/web")
sys.path.append("/home/pi/MarsRover/marsrovercore")
from web import app, rover
import logging
import os
import datetime

# create root logger
root_logger = logging.getLogger("Root-Web")
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s")
# console logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
root_logger.addHandler(ch)
# file logging
filelogger_dir_name = "logfiles"
current_dir = os.getcwd()
filelogger_dir = rf"{current_dir}/{filelogger_dir_name}"
if not os.path.isdir(filelogger_dir):
    os.mkdir(filelogger_dir)
logfile_name = f"MarsRover_{datetime.date.today().strftime('%d-%m-%Y')}.log"
logfile_path = rf"{filelogger_dir}/{logfile_name}"
fh = logging.FileHandler(logfile_path)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
root_logger.addHandler(fh)

try:
    root_logger.critical('START')
    rover.take_default_position()
    rover.drive_speed = 0.3
    # run flask app
    app.run(host='0.0.0.0', port=8181)
except KeyboardInterrupt:
    root_logger.critical("exit triggered by KEYBOARDINTERRUPT")
except Exception as ex:
    root_logger.critical("exit triggered by EXCEPTION")
    root_logger.exception(ex)
finally:
    if rover:
        rover.pull_handbreak()
        rover.gpio.cleanup_all()
    root_logger.critical('END \n------------------------------------------------------------------')

