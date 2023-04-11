import math
import time
import pigpio
import threading
import numpy as np
from website.calcs.inverse_kinematics import inverse_kinematics

pi = pigpio.pi()
#pi.set_mode(12, pigpio.OUTPUT)
pins = {'base': 12, 'shoulder': 13, 'elbow': 7, 'wrist': 8, 'wrist_rot': 4, 'gripper': 5}
angles = {'base': 90, 'shoulder': 90, 'elbow': 90, 'wrist': 90, 'wrist_rot': 90, 'gripper': 90}

def angle_to_pulsewidth(angle):
    return 500 + int(angle / 180 * 2000)

def pulsewidth_to_angle(pulsewidth):
    return (pulsewidth - 500)/2000 * 180

def sine_smooth_servo(servo_pin, start_angle, end_angle):
    # Calculate the range of motion and the maximum x value
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
        print(y_max)
        print(y_min)
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
        if data[part] != angles[part]:
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
    angles['shoulder'] = angles['shoulder'] - 24; 
    angles['elbow'] = angles['elbow'] - 121; 
    angles['wrist'] = angles['wrist'] - 90; 
    return True

def servoto_coordinates(x, y, z):
    ang = inverse_kinematics(x, y, z)

    print(ang)
    if ang is not None:
        threads = list()
        tmp = ang.copy()
        ang['shoulder'] = np.abs(-24 - ang['shoulder'])
        ang['elbow'] = np.abs(-121 - ang['elbow'])
        ang['wrist'] = np.abs(-90 - ang['wrist'])
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