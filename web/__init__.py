from flask import Flask
from marsrovercore.marsrover import MarsRover

app = Flask(__name__)
rover: MarsRover = MarsRover(camera_enabled=False)

import routes