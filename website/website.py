from flask import render_template, Blueprint, request, jsonify, redirect
from website.model.repositories import *
from website.model.robot_controll import *
import pigpio
import time

pi = pigpio.pi()
servo_pin = 12   # The GPIO pin connected to the servo

# Set the servo pin to output mode
website_api = Blueprint('website', __name__)
global base


#pi.set_mode(servo_pin, pigpio.OUTPUT)

#pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(base))

@website_api.route('/',  methods=["GET", "POST"])
def website():
    toSend = get_angles()
    return render_template("website.html", toSend = toSend)

@website_api.route('/move',  methods=["GET", "POST"])
def move():
    data = request.get_json()  # parse JSON data from request body
    print(data)
    if 'x' in data:
        if not servoto_coordinates(float(data['x']), float(data['y']), float(data['z'])):
            message = "Selected coordinates are out of work space!"
            return render_template("website.html", message = message)
    else:
        parts = get_changes(data)
        move_servo(parts, data)
    toSend = get_angles()
    return jsonify(toSend)  # return angles as JSON
    