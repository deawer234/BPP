import math
import time
import pigpio

def sine_smooth_servo(servo_pin, frequency, amplitude, num_samples, target_angle):
    # Set up the GPIO pins
    pi = pigpio.pi()

    # Calculate the time interval between samples based on frequency
    t_interval = 1 / frequency

    # Create an array of angles to move the servo to
    if num_samples > 1:
        angles = [0] * num_samples
        for i in range(num_samples):
            angles[i] = math.sin(2 * math.pi * frequency * i * t_interval) * amplitude + 1500
    else:
        angles = [target_angle]

    # Move the servo to each angle in the array
    for angle in angles:
        pi.set_servo_pulsewidth(servo_pin, angle)
        time.sleep(0.02)

    # Clean up the GPIO pins
    pi.stop()