from crypt import methods
from marsrovercore.marsrover import WheelPosition, DriveDirection
from web import app, rover
from flask import render_template, jsonify

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Mars Rover Webcontrol")

@app.route('/get_status/', methods=['GET'])
def get_status():
    return jsonify(rover.get_status())

@app.route('/get_sensor_measures/', methods=['GET'])
def get_sensor_measures(): 
    return jsonify(rover.sensorcontroller.get_meteo_light_measures(round_measure_by=1))

@app.route('/shutdown/', methods=['POST'])
def shutdown():
    rover.shutdown()
    ret_data = {"value": "shutdown pi"}
    return jsonify(ret_data)  

@app.route('/reboot/', methods=['POST'])
def reboot():
    rover.reboot() 
    ret_data = {"value": "reboot pi"}
    return jsonify(ret_data) 
   
@app.route('/forward_start/', methods=['POST'])
def forward_start():
    rover.drive_direction = DriveDirection.FORWARD
    rover.start_drive()
    ret_data = {"value": "forward start"}
    return jsonify(ret_data)
      
@app.route('/reverse_start/', methods=['POST'])
def reverse_start():
    rover.drive_direction = DriveDirection.REVERSE
    rover.start_drive()
    ret_data = {"value": "reverse stop"}
    return jsonify(ret_data)

@app.route('/stop/', methods=['POST'])
def stop():
    rover.stopdrive()
    ret_data = {"value": "stop"}
    return jsonify(ret_data)

@app.route('/wheel_position/<position>', methods=['POST'])
def wheelposition(position):
    wheelposition: WheelPosition = WheelPosition[position]
    rover.setwheelposition(wheelposition)

    ret_data = {"value": f"{wheelposition.name} wheel position"}
    return jsonify(ret_data)

@app.route('/point_front_camera/<degree>', methods=['POST'])
def point_front_camera(degree):
    todegree: int = int(degree)
    rover.front_camera.point(todegree)
    ret_data = {"value": f"point camera to {todegree}"}
    return jsonify(ret_data)

@app.route('/start_distance_measure/', methods=['POST'])
def start_distance_measure():
    state: str
    if rover.distancemeasure_running:
        rover.stop_distance_measure()
        state = "stop"
    else:
        rover.start_distance_measure()
        state = "start"
    ret_data = {"value": f"{state} distance measure"}
    return jsonify(ret_data)

@app.route('/set_speed/<speed>', methods=['POST'])
def set_speed(speed):
    new_speed = int(speed) / 100
    rover.drive_speed = new_speed
    ret_data = {"value": f"set speed to {new_speed}"}
    return jsonify(ret_data)