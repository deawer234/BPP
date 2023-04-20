from flask import render_template, Blueprint, request, jsonify, redirect, Response, stream_with_context
from website.model.repositories import *
from website.model.robot_controll import *
from website.model.repositories import *
import pigpio
import time
import pigpio

# Set the servo pin to output mode
website_api = Blueprint('index', __name__)
init_motors()

@website_api.route('/',  methods=["GET", "POST"])
def website():
    
    tabs = get_tabs()
    positions = {}
    tabInfo = {}
    for tab in tabs:
        tmp = []
        tabInfo[tab.movement_id] = tab.name
        pos = get_positions_of_tab(tab.movement_id)
        for position in pos:
            data = {
                "position_id": position.position_id,
                "base": position.base,
                "shoulder": position.shoulder,
                "elbow": position.elbow,
                "wrist": position.wrist,
                "wrist_rot": position.wrist_rot,
                "gripper": position.gripper
            }
            tmp.append(data)
        positions[tab.movement_id] = tmp
    print(positions)
    print(tabInfo)
    currentPos = get_angles()
    return render_template("index.html", data = positions, tabInfo = tabInfo, currentPos = currentPos)

@website_api.route('/move',  methods=["GET", "POST"])
def move():
    data = request.get_json()  # parse JSON data from request body
    print(data)
    if 'x' in data:
        if not servoto_coordinates(float(data['x']), float(data['y']), float(data['z'])):
            message = "Selected coordinates are out of work space!"
            return jsonify(message)
    else:
        parts = get_changes(data)
        print(parts)
        move_servo(parts, data)
    toSend = get_angles()
    return jsonify(toSend)  # return angles as JSON

@website_api.route('/add_position', methods=["GET", "POST"])
def add_pos():
    data = request.get_json()
    add_positon(data['movement_id'], data)
    response = {'status': 'success', 'message': 'Operation completed successfully.'}
    return jsonify(response), 200

@website_api.route('/add_tab', methods=["GET", "POST"])
def add_tabs():
    data = request.get_json()
    print(data)
    add_tab(data['movement_id'], data['name'])
    response = {'status': 'success', 'message': 'Operation completed successfully.'}
    return jsonify(response), 200

@website_api.route('/remove_tab', methods=["GET", "POST"])
def rem_tab():
    data = request.get_json()
    print(data)
    remove_tab(data)
    response = {'status': 'success', 'message': 'Operation completed successfully.'}
    return jsonify(response), 200

@website_api.route('/remove_pos', methods=["GET", "POST"])
def remove_pos():
    data = request.get_json()
    print(data)
    print(get_position(str(data)))
    remove_position(data)
    response = {'status': 'success', 'message': 'Operation completed successfully.'}
    return jsonify(response), 200

@website_api.route('/play', methods=["GET", "POST"])
def play():
    data = request.get_json()
    print(data)
    servos = get_changes(data)
    move_servo(servos, data)
    time.sleep(2)
    return jsonify(get_angles())

@website_api.route('/display', methods=["GET", "POST"])
def display():
    data = request.get_json()
    message = get_display_of(float(data['x']), float(data['y']), float(data['z']))
    return jsonify(message)