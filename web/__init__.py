from flask import Flask
from marsrovercore.marsrover import MarsRover
import logging

app = Flask(__name__)
rover: MarsRover = MarsRover(camera_enabled=False)
logger: logging.Logger = logging.getLogger('MarsRover.Web')

import routes

