"""
Module for communicating with GPIO ports and ensuring robot controll.

Author: Daniel Němec
Date: 15.03.2023

Python Version: 3.8.10
"""

import math
import time
import pigpio
import threading
import numpy as np
import os, json
from website.calcs.kinematics import inverse_kinematics
from website.calcs.kinematics import forward_kinematics

#CHANGE NUMBER OF THE PIN IF YOU'VE CHANGED ANY PINS
pins = {'base': 17, 'shoulder': 12, 'elbow': 27, 'wrist': 22, 'wrist_rot': 23, 'gripper': 24}

# Definition of the file last_pos.json to load last position of the arm
file_path = os.path.join('./website/database', 'last_pos.json')

if os.path.isfile(file_path):
    with open(file_path, 'r') as f:
        angles = json.load(f)
else:
    angles = {'base': 90, 'shoulder': 66, 'elbow': -31, 'wrist': -25, 'wrist_rot': 90, 'gripper': 90}

pi = pigpio.pi()

def write_to_file():
    with open(file_path, 'w') as f:
        json.dump(angles, f, indent=4)
    
def angle_to_pulsewidth(angle):
    return 600 + int(angle / 180 * 1850)

def pulsewidth_to_angle(pulsewidth):
    return (pulsewidth - 500)/2000 * 180

#Init of the servo motors
def init_motors():
    tmp = angles.copy()
    for servo in pins:
        if servo == 'shoulder':
            tmp['shoulder'] = tmp['shoulder'] + 24
        elif servo == 'elbow':
            tmp['elbow'] = tmp['elbow'] + 121
            tmp['elbow'] = 180 - tmp['elbow']
        elif servo == 'wrist':
            tmp['wrist'] = tmp['wrist'] + 115
        #COMMENT TWO LINES BELOW FOR NON RASPBERRY PI USAGE
        pi.set_mode(pins[servo], pigpio.OUTPUT)
        pi.set_servo_pulsewidth(pins[servo], angle_to_pulsewidth(tmp[servo]))
    return

def sine_smooth_servo(servo_pin, start_angle, end_angle, num_steps):
    # Adjusts start and end angles based on servo pin
    if servo_pin == pins['shoulder']:
        start_angle = start_angle + 24
        end_angle = end_angle + 24
    elif servo_pin == pins['elbow']:
        start_angle = start_angle + 121
        end_angle = end_angle + 121
        start_angle = 180 - start_angle
        end_angle = 180 - end_angle
    elif servo_pin == pins['wrist']:
        start_angle = start_angle + 115
        end_angle = end_angle + 115

    x_max = abs(end_angle - start_angle)  # Calculates the difference between the start and end angles

    x_values = np.linspace(int(start_angle), int(end_angle), int(num_steps))  # Creates a list of equally spaced x values

    mapped_positions = []
    if x_max != 0:
        # Calculates y values using sine function
        y_values = [x_max/2 * math.sin((( math.pi * (x - start_angle)) / ( x_max)) - 0.5 * math.pi) + x_max/2 for x in x_values]
        
        # Maps y values to the corresponding x values and adds them to a list
        mapped_positions = [(y - min(y_values)) / (x_max) * (end_angle - start_angle) + start_angle for y in y_values]
    
    for position in mapped_positions:
        #COMMENT LINE BELOW FOR NON RASPBERRY PI USAGE
        pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(position))
        time.sleep(0.02)  # Pauses for 20ms

    return

def get_changes(data):
    changes = []
    for part in data:
        if int(data[part]) != angles[part]:
            changes.append(part)
    return changes

def move_servo(data):
    # This function takes in a dictionary `data` that represents the angles for all parts, and moves each part's
    # corresponding servo motor smoothly to reach the desired angle.
    threads = list()
    setSpeed = float(data.pop('speed'))
    # `setSpeed` is the speed at which the servo motors will move.
    # `data` contains the desired angles for all parts.
    # We remove the `speed` key from `data` since we don't need it anymore.
    parts = get_changes(data)
    # We get the list of parts that have changed compared to the current `angles` dictionary.
    speed = []
    num_samples=0
    for part in parts:
        # We calculate the difference in angles between the current angle and the desired angle for each part.
        speed.append(np.abs(angles[part]-int(data[part])))
    if speed:
        # If there are any parts that need to be moved, we calculate the number of samples needed for each part to
        # move smoothly to the desired angle.
        num_samples = max(speed)
        num_samples = num_samples / setSpeed
    for part in parts:
        # We create a new thread for each part that needs to be moved.
        # The `sine_smooth_servo` function is called with the current angle for the part, the desired angle for the part,
        # and the number of samples needed for the part to move smoothly.
        x = threading.Thread(target=sine_smooth_servo, args=(pins[part], angles[part], int(data[part]), num_samples))
        threads.append(x)
        x.start()
        angles[part] = int(data[part])
    for _, thread in enumerate(threads):
        # We wait for all the threads to finish executing.
        thread.join()
    # We write the new angles to the `filename` file.
    write_to_file()
    return True

def servoto_coordinates(x, y, z, setSpeed):
    # This function takes in the coordinates (x, y, z) and moves the arm to reach that position.
    ang = inverse_kinematics(x, y, z, angles)
    # We calculate the angles required for all parts to reach the position (x, y, z).
    # `ang` is a dictionary containing the angles for all parts.
    parts = get_changes(ang)
    speed = []
    num_samples=0
    for part in parts:
        # We calculate the difference in angles between the current angle and the desired angle for each part.
        speed.append(np.abs(angles[part]-int(ang[part])))
    if speed:
        # If there are any parts that need to be moved, we calculate the number of samples needed for each part to
        # move smoothly to the desired angle.
        num_samples = max(speed)
        num_samples = num_samples / setSpeed
    if ang is not None:
        # If we have calculated the angles successfully, we move each part's corresponding servo motor smoothly to reach
        # the desired angle.
        threads = list()
        tmp = ang.copy()
            # We create a new thread for each part that needs to be moved.
        for servo in pins:
            x = threading.Thread(target=sine_smooth_servo, args=(pins[servo], angles[servo], ang[servo], num_samples))
            threads.append(x)
            x.start()
            angles[servo] = tmp[servo]
        for i, thread in enumerate(threads):
            thread.join()
        write_to_file()
    else:
        return False
    return True

# Linear interpolatin between two points in 3D
def linear_interpolation(p_start, p_end, n_steps):
    return np.array([p_start + (i/n_steps) * (p_end - p_start) for i in range(n_steps+1)])


# Defining barrier for the threads to wait for each other
barrier = threading.Barrier(6)

#LINE MOVEMENT
def servoto_coordinates_line(x, y, z, speed):
    # Getting the starting point in coordinates using FK
    start_point = forward_kinematics(angles['base'], angles['shoulder'], angles['elbow'], angles['wrist'])
    # Linear interpolation of hte 2 points
    points = linear_interpolation(start_point, np.array([x, y, z]), int(100 / speed))
    joint_angles = []
    # Calculating IK for each of the point from the linear interpolation
    for p in points:
        if joint_angles and joint_angles is not None:
            solution = inverse_kinematics(p[0], p[1], p[2], joint_angles[-1])
        else:
            solution = inverse_kinematics(p[0], p[1], p[2], angles)
        if solution is not None:
            joint_angles.append(solution)
    
    threads = list()
    # We create a new thread for each part that needs to be moved.
    for servo in pins:
        x = threading.Thread(target=move_line, args=(servo, joint_angles))
        threads.append(x)
        x.start()
        angles[servo] = joint_angles[-1][servo]
    for i, thread in enumerate(threads):
        thread.join()
    write_to_file()
    return True

def move_line(servo, angl):
    
    for i in range(len(angl)):
        if servo == 'shoulder':
            angl[i][servo] = angl[i][servo] + 24
        elif servo == 'elbow':
            angl[i][servo] =  angl[i][servo]  + 121
            angl[i][servo] = 180 - angl[i][servo] 
        elif servo =='wrist':
            angl[i][servo] = angl[i][servo]  + 115
        
        
        pi.set_servo_pulsewidth(pins[servo], angle_to_pulsewidth(angl[i][servo]))
        time.sleep(0.02)
        barrier.wait()
    return 

# Get current angles of the arm
def get_angles():
    return angles

# Displaying x y z without moving
def get_display_of(x, y, z):
    return inverse_kinematics(x, y, z, angles)




