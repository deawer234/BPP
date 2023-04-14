import math
import time
import pigpio
import threading
import numpy as np
from website.calcs.inverse_kinematics import inverse_kinematics

pins = {'base': 13, 'shoulder': 12, 'elbow': 27, 'wrist': 22, 'wrist_rot': 4, 'gripper': 5}
angles = {'base': 90, 'shoulder': 66, 'elbow': -31, 'wrist': 0, 'wrist_rot': 90, 'gripper': 90}

pi = pigpio.pi()

def angle_to_pulsewidth(angle):
    return 500 + int(angle / 180 * 2000)

def pulsewidth_to_angle(pulsewidth):
    return (pulsewidth - 500)/2000 * 180

def init_motors():
    #for servo in pins:
        #pi.set_mode(pins[servo], pigpio.OUTPUT)
        #pi.set_servo_pulsewidth(pins[servo], angle_to_pulsewidth(90))
    return
    
    # threads = list()
    # start = get_current_angles()
    # for servo in pins:
    #     x = threading.Thread(target=sine_smooth_servo, args=(pins[servo], start[servo], angles[servo]))
    #     #sine_smooth_servo(pins[part], angles[part], int(data[part]))
    #     threads.append(x)
    #     x.start()
    # for _, thread in enumerate(threads):
    #     thread.join()

def sine_smooth_servo(servo_pin, start_angle, end_angle):
    #print("start angle " + str(start_angle))
    #print("target angle " + str(end_angle))
    # Calculate the range of motion and the maximum x value
    if servo_pin == pins['shoulder']:
        start_angle = start_angle + 24
        end_angle = end_angle + 24
    elif servo_pin == pins['elbow']:
        start_angle = start_angle + 121
        end_angle = end_angle + 121
    elif servo_pin == pins['wrist']:
        start_angle = start_angle + 90
        end_angle = end_angle + 90
    x_max = abs(end_angle - start_angle)
    # Generate the y-values using the sine function
    if(start_angle < end_angle):
        y_values = [x_max * math.sin((0.5 * math.pi * (x - start_angle)) / (0.5 * x_max) + 0.5 * math.pi) + x_max for x in range(start_angle, end_angle)]
        y_values.reverse()
    else:
        y_values = [x_max * math.sin((0.5 * math.pi * (start_angle - x)) / (0.5 * x_max) + 0.5 * math.pi) + x_max for x in range(end_angle, start_angle)]

    # Map the y values to the appropriate servo positions
    if y_values:
        y_min = min(y_values)
        y_max = max(y_values)
        if y_max == y_min and y_max != 0:
            mapped_positions = [(y - y_min) / (y_max) * (end_angle - start_angle) + start_angle for y in y_values]
        else:
            mapped_positions = [(y - y_min) / (y_max - y_min) * (end_angle - start_angle) + start_angle for y in y_values]
        # Move the servo to the mapped positions
            for position in mapped_positions:
                #pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(position))
                time.sleep(0.02)  # Wait for the servo to move to the new position

def get_changes(data):
    changes = []
    for part in data:
        if int(data[part]) != angles[part]:
            changes.append(part)
    return changes

def move_servo(parts, data):
    threads = list()
    for part in parts:
        x = threading.Thread(target=sine_smooth_servo, args=(pins[part], angles[part], int(data[part])))
        #sine_smooth_servo(pins[part], angles[part], int(data[part]))
        threads.append(x)
        x.start()
        angles[part] = int(data[part])
    for _, thread in enumerate(threads):
        thread.join()
    return True

def servoto_coordinates(x, y, z):
    
    ang = inverse_kinematics(x, y, z)
    print("before")
    print(angles)
    print("after")
    print(ang)
    if ang is not None:
        threads = list()
        tmp = ang.copy()
        for servo in pins:
            x = threading.Thread(target=sine_smooth_servo, args=(pins[servo], angles[servo], ang[servo]))
            #sine_smooth_servo(pins[part], angles[part], int(data[part]))
            threads.append(x)
            x.start()
            #sine_smooth_servo(pins[servo], angles[servo], ang[servo])
            angles[servo] = tmp[servo]
        for _, thread in enumerate(threads):
            thread.join()
    else:
        return False
    return True

def get_angles():
    return angles