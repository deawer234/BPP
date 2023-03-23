from flask import render_template, Blueprint, request, jsonify
import pigpio

website_api = Blueprint('website', __name__)

pi = pigpio.pi()

base = 90
shoulder = 90
forearm = 90
elbow = 90
wrist = 90
gripper = 90

@website_api.route('/',  methods=["GET", "POST"])
def website():

    return render_template("website.html")

@website_api.route('/move',  methods=["POST"])
def move():
    data = request.get_json()  # parse JSON data from request body
    # do something with data
    print(data)
    response = {'message': 'Success'}

    return jsonify(response)