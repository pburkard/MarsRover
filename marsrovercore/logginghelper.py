import logging
import datetime
import os

root_logger: logging.Logger = None
filelogger_dir_name = "logfiles"

def create_logger(name: str) -> logging.Logger:
    global root_logger
    if root_logger == None:
        root_logger = logging.getLogger(name)
        root_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s")
        # console logging
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)
        # file logging
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
    return root_logger

def get_logger(name: str) -> logging.Logger:
    global root_logger
    if root_logger == None:
        raise Exception("init root logger first")
    return logging.getLogger(f"MarsRover.{name}")