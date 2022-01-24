from tokenize import String
import marsrover
from time import sleep
from flask import Flask, render_template, jsonify, request

rover: marsrover.MarsRover
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Mars Rover Webcontrol")

@app.route('/get_status/', methods=['GET'])
def status():
    return jsonify(rover.get_status())

@app.route('/get_environment_measures/', methods=['GET'])
def get_environment_measures():    
    return jsonify(rover.environment_hat.get_all_measures(round_decimal_place=1))

@app.route('/shutdown/', methods=['POST'])
def shutdown():
    rover.shutdownpi()
    ret_data = {"value": "shutdown pi"}
    return jsonify(ret_data)  

@app.route('/reboot/', methods=['POST'])
def reboot():
    rover.rebootpi()  
    ret_data = {"value": "reboot pi"}
    return jsonify(ret_data) 
   
@app.route('/forward_start/', methods=['POST'])
def forward_start():
    rover.driveDirection = marsrover.DriveDirection.FORWARD
    rover.drive()
    ret_data = {"value": "forward start"}
    return jsonify(ret_data)
      
@app.route('/reverse_start/', methods=['POST'])
def reverse_start():
    rover.driveDirection = marsrover.DriveDirection.REVERSE
    rover.drive()
    ret_data = {"value": "reverse stop"}
    return jsonify(ret_data)

@app.route('/stop/', methods=['POST'])
def stop():
    rover.stopdrive()
    ret_data = {"value": "stop"}
    return jsonify(ret_data)

@app.route('/wheel_position/<position>', methods=['POST'])
def wheelposition(position):
    wheelposition: marsrover.WheelPosition = marsrover.WheelPosition[position]
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
    state: String
    if rover.distancemeasure_running:
        rover.stop_distance_measure()
        state = "stop"
    else:
        rover.start_distance_measure()
        state = "start"
    ret_data = {"value": f"{state} distance measure"}
    return jsonify(ret_data)

if(__name__ == '__main__'):
    rover = marsrover.MarsRover(camera_enabled=False)
    rover.logger.critical('START')
    rover.logger.critical(f'mode: {marsrover.StartMode.WEBCONTROL.name}')
    try:
        rover.takeDefaultPosition()
        # run flask app
        app.run(host='0.0.0.0', port=8181, debug=False)
    finally:
        rover.pullHandbreak()
        sleep(1)
        rover.cleanup()
        rover.logger.critical('END \n------------------------------------------------------------------')

