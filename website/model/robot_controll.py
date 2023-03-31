import math
import time
import pigpio
from website.calcs.inverse_kinematics import inverse_kinematics

pi = pigpio.pi()
#pi.set_mode(12, pigpio.OUTPUT)

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
    y_min = min(y_values)
    y_max = max(y_values)
    mapped_positions = [(y - y_min) / (y_max - y_min) * (end_angle - start_angle) + start_angle for y in y_values]
    # Move the servo to the mapped positions
    for position in mapped_positions:
        #pi.set_servo_pulsewidth(servo_pin, angle_to_pulsewidth(position))
        time.sleep(0.02)  # Wait for the servo to move to the new position

def servoto_coordinates(x, y, z):
    q = inverse_kinematics(x, y, z)
    print(q)
