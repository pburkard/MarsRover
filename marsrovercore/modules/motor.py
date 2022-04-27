import marsrovercore.logginghelper as logginghelper
from marsrovercore.enums import ServoDriverChannel

class Motor():
    def __init__(self, name:str, channel: ServoDriverChannel):
        self.logger = logginghelper.get_logger(f"{Motor.__name__}.{name}")
        self.name = name

    # to be implemented...