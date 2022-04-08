# import sys
# sys.path.append("/home/pi/MarsRover/marsrovercore")

import logging
import os
import datetime
root_logger = logging.getLogger("MarsRover")
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

from marsrovercore.marsrover import MarsRover
rover: MarsRover = MarsRover(camera_enabled=False)
rover.drive_speed = 0.6