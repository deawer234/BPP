import math
import time
import pigpio
import threading
import numpy as np

def sine_smooth_continuous_servo(servo_pin, start_angle, target_angle, num_steps=100):
    # Calibrate these values for your servo
    stop_pulse_width = 1500
    clockwise_pulse_width = 1450
    counterclockwise_pulse_width = 1550
    time_per_degree = 0.14 / 60  # The time it takes for the servo to rotate one degree at the chosen speed

    # Determine the direction and pulse width based on the target angle
    if target_angle > start_angle:
        pulse_width = clockwise_pulse_width
    else:
        pulse_width = counterclockwise_pulse_width
        #target_angle = -target_angle  # Make the target_angle positive for calculation

    target_angle = target_angle - start_angle

    x_max = target_angle
    x_values = np.linspace(0, x_max, num=num_steps)
    y_values = [x_max/2 * math.sin(((math.pi * x) / x_max) - 0.5 * math.pi) + x_max/2 for x in x_values]

    # Calculate the time intervals between steps
    time_intervals = [time_per_degree * (y2 - y1) for y1, y2 in zip(y_values[:-1], y_values[1:])]

    total_time = time_per_degree * target_angle
    time_intervals = [interval * (total_time / sum(time_intervals)) for interval in time_intervals]
    # Send the pulse width to start the servo rotation
    # pi.set_servo_pulsewidth(servo_pin, pulse_width)
    print(time_intervals)
    # Move the servo through the sine wave pattern
    for interval in time_intervals:
        time.sleep(interval)

    # Send the stop pulse width to stop the servo rotation
    # pi.set_servo_pulsewidth(servo_pin, stop_pulse_width)

    return

sine_smooth_continuous_servo(18, 180, 360, num_steps=100)