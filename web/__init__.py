from flask import Flask
from marsrovercore.marsrover import MarsRover

app = Flask(__name__)
rover: MarsRover = MarsRover(camera_enabled=False)
rover.drive_speed = 0.6

import routes