import logging
import datetime
import os

root_logger: logging.Logger = None

def create_logger(name: str, levelConsole) -> logging.Logger:
    global root_logger
    if root_logger == None:
        root_logger = logging.getLogger(name)
        root_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s")
        # console logging
        ch = logging.StreamHandler()
        ch.setLevel(levelConsole)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)
        # file logging
        currentDirectory = os.getcwd()
        fileName = f"MarsRover_{datetime.date.today().strftime('%d-%m-%Y')}.log"
        file = rf"{currentDirectory}/logfiles/{fileName}"
        print(file)
        try:
            fh = logging.FileHandler(file)
            fh.setFormatter(formatter)
            fh.setLevel(logging.DEBUG)
            root_logger.addHandler(fh)
        except Exception as ex:
            raise ex
    return root_logger

def get_logger(name: str) -> logging.Logger:
    global root_logger
    if root_logger == None:
        raise Exception("init root logger first")
    return logging.getLogger(f"MarsRover.{name}")