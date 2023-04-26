import math
import time
import pigpio
import threading
import numpy as np
from website.calcs.inverse_kinematics import inverse_kinematics
from website.calcs.forward_kinematics import forward_kinematics


pins = {'base': 17, 'shoulder': 12, 'elbow': 27, 'wrist': 22, 'wrist_rot': 23, 'gripper': 24}
angles = {'base': 90, 'shoulder': 66, 'elbow': -31, 'wrist': -25, 'wrist_rot': 90, 'gripper': 90}

pi = pigpio.pi()

def angle_to_pulsewidth(angle):
    return 600 + int(angle / 180 * 1850)

def pulsewidth_to_angle(pulsewidth):
    return (pulsewidth - 500)/2000 * 180

def init_motors():
    #for servo in pins:
        #pi.set_mode(pins[servo], pigpio.OUTPUT)
        #pi.set_servo_pulsewidth(pins[servo], angle_to_pulsewidth(90))
    return

def sine_smooth_servo(servo_pin, start_angle, end_angle, num_steps):
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

    x_max = abs(end_angle - start_angle)

    # Generate an array with equal steps between start_angle and end_angle

    x_values = np.linspace(int(start_angle), int(end_angle), int(num_steps))

    mapped_positions = []
    if x_max != 0:
        y_values = [x_max/2 * math.sin((( math.pi * (x - start_angle)) / ( x_max)) - 0.5 * math.pi) + x_max/2 for x in x_values]
        
    
        mapped_positions = [(y - min(y_values)) / (x_max) * (end_angle - start_angle) + start_angle for y in y_values]
    
    for position in mapped_positions:
        #pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(position))
        time.sleep(0.02)  # Wait for the servo to move to the new position with the adjusted delay

    return

def get_changes(data):
    changes = []
    for part in data:
        if int(data[part]) != angles[part]:
            changes.append(part)
    return changes

def move_servo(data):
    threads = list()
    print(data)
    setSpeed = float(data.pop('speed'))
    parts = get_changes(data)
    speed = []
    num_samples=0
    for part in parts:
        speed.append(np.abs(angles[part]-int(data[part])))
    if speed:
        num_samples = max(speed)
        num_samples = num_samples / setSpeed
    for part in parts:
        x = threading.Thread(target=sine_smooth_servo, args=(pins[part], angles[part], int(data[part]), num_samples))
        #sine_smooth_servo(pins[part], angles[part], int(data[part]))
        threads.append(x)
        x.start()
        angles[part] = int(data[part])
    for _, thread in enumerate(threads):
        thread.join()
        print(thread)
    print(time.gmtime())
    return True

def servoto_coordinates(x, y, z, setSpeed):
    ang = inverse_kinematics(x, y, z, angles)
    parts = get_changes(ang)
    speed = []
    num_samples=0
    for part in parts:
        speed.append(np.abs(angles[part]-int(ang[part])))
    if speed:
        num_samples = max(speed)
        num_samples = num_samples / setSpeed
    if ang is not None:
        threads = list()
        tmp = ang.copy()
        for servo in pins:
            x = threading.Thread(target=sine_smooth_servo, args=(pins[servo], angles[servo], ang[servo], num_samples))
            threads.append(x)
            x.start()
            angles[servo] = tmp[servo]
        for i, thread in enumerate(threads):
            thread.join()
    else:
        return False
    return True

def linear_interpolation(p_start, p_end, n_steps):
    return np.array([p_start + (i/n_steps) * (p_end - p_start) for i in range(n_steps+1)])

#LINE MOVEMENT
barrier = threading.Barrier(6)
def servoto_coordinates_line(x, y, z, speed):
    # ang = inverse_kinematics(x, y, z, angles)
    # if ang is None:
    #     return False
    start_point = forward_kinematics(np.radians(angles['base']), np.radians(angles['shoulder']), np.radians(angles['elbow']), np.radians(angles['wrist']))
    points = linear_interpolation(np.array([x, y, z]), start_point, 100 / speed)
    points = points[::-1]
    # Calculate joint angles for each point
    joint_angles = []
    for p in points:
        if joint_angles and joint_angles is not None:
            print(joint_angles[-1])
            print(p[0], p[1], p[2])
            joint_angles.append(inverse_kinematics(p[0], p[1], p[2], joint_angles[-1]))
        else:
            joint_angles.append(inverse_kinematics(p[0], p[1], p[2], angles))
    # joint_angles = [inverse_kinematics(p[0], p[1], p[2], angles) for p in points]   
    # tmp = joint_angles[-1]
    # Move the robotic arm through the joint angle configurations
    
    
    
    # print(start_point)
    # p1 = np.array([start_point['x'], start_point['y'], start_point['z']])
    # p2 = np.array([x, y, z])
    # points = interpolate_points(p1, p2)
    # print(points)
    # for point in range(len(points)):
        # parts = get_changes(angl)
        # speed = []
        # num_samples = 0;
        # for part in parts:
        #     speed.append(np.abs(angles[part]-int(angl[part])))
        # if speed:
        #     num_samples = max(speed)
    
    threads = list()
    for servo in pins:
        x = threading.Thread(target=lol, args=(servo, joint_angles))
        threads.append(x)
        x.start()
        angles[servo] = joint_angles[-1][servo]
    for i, thread in enumerate(threads):
        thread.join()
    #print(angles)
    return True

def lol(servo, angl):
    for i in range(len(angl)):
        # if i != 0 and (angl[i][servo] > (angl[i-1][servo] + 5) or angl[i][servo] + 5 < (angl[i-1][servo])):
        #     sine_smooth_servo(pins[servo], angl[i-1][servo], angl[i][servo], int(np.abs((np.abs(angl[i][servo]) - np.abs(angl[i-1][servo])))));
        #     continue
        if servo == 'shoulder':
            angl[i][servo] = angl[i][servo] + 24
        elif servo == 'elbow':
            angl[i][servo] = angl[i][servo]  + 121
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




