import math
import time
import pigpio
import threading
import numpy as np
from website.calcs.inverse_kinematics import inverse_kinematics

pins = {'base': 18, 'shoulder': 12, 'elbow': 27, 'wrist': 22, 'wrist_rot': 23, 'gripper': 24}
angles = {'base': 100, 'shoulder': 66, 'elbow': -31, 'wrist': 0, 'wrist_rot': 90, 'gripper': 90}

pi = pigpio.pi()

def angle_to_pulsewidth(angle):
    return 500 + int(angle / 180 * 2000)

def pulsewidth_to_angle(pulsewidth):
    return (pulsewidth - 500)/2000 * 180

def init_motors():
    # for servo in pins:
    #     pi.set_mode(pins[servo], pigpio.OUTPUT)
    #     # if servo = 'base':
    #     #     pi.set_servo_pulsewidth(pins[servo], angle_to_pulsewidth(180))
    #     pi.set_servo_pulsewidth(pins[servo], angle_to_pulsewidth(90))
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
        y_values = [x_max/2 * math.sin((( math.pi * (x - start_angle)) / ( x_max)) - 0.5 * math.pi) + x_max/2 for x in range(start_angle, end_angle)]
    else:
        y_values = [x_max/2 * math.sin((( math.pi * (start_angle - x)) / (x_max)) - 0.5 * math.pi) + x_max/2 for x in range(end_angle, start_angle)]
        y_values.reverse()
    print(y_values)
    # Map the y values to the appropriate servo positions
    mapped_positions=[]
    if y_values:
        y_min = min(y_values)
        y_max = max(y_values)
        
        if y_max == y_min and y_max != 0:
            mapped_positions = [end_angle]
        else:
            mapped_positions = [(y - y_min) / (x_max) * (end_angle - start_angle) + start_angle for y in y_values]
        # Move the servo to the mapped positions
    for position in mapped_positions:
        # pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(position))
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
            threads.append(x)
            x.start()
            angles[servo] = tmp[servo]
        for _, thread in enumerate(threads):
            thread.join()
    else:
        return False
    return True

def get_angles():
    return angles

def get_display_of(x, y, z):
    return inverse_kinematics(x, y, z)

# def move_inline(point1, point2):
#     m = point2['y'] - point1[]