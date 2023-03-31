from flask import render_template, Blueprint, request, jsonify
from website.model.robot_controll import sine_smooth_servo, servoto_coordinates, angle_to_pulsewidth
import pigpio
import time

pi = pigpio.pi()
servo_pin = 12   # The GPIO pin connected to the servo

# Set the servo pin to output mode
website_api = Blueprint('website', __name__)
global base

shoulder = 90
forearm = 90
elbow = 90
wrist = 90
gripper = 90
base = 0

#pi.set_mode(servo_pin, pigpio.OUTPUT)

#pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(base))

@website_api.route('/',  methods=["GET", "POST"])
def website():

    return render_template("website.html")

@website_api.route('/move',  methods=["POST"])
def move():
    global base
    data = request.get_json()  # parse JSON data from request body
    #pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(180))
    sine_smooth_servo(servo_pin, base, int(data['base']))
    base = int(data['base'])

    response = {'message': 'Success'}

    return jsonify(response)

@website_api.route("/move/coordinates", methods=["POST"])
def move_inverse_kinematics():
    data = request.get_json()
    print(data)
    
    angles = servoto_coordinates(float(data['x']), float(data['y']), float(data['z']))

    response = {'message': 'Success'}

    return jsonify(response)

