import math

xmax = 180  # maximum angle of servo
default_time = 0.160  # time to rotate from 0 to 60 degrees
angle_increment = 60  # angle increment
n_points = 180  # number of points to compute duty cycle

# compute time intervals and duty cycles
dt = default_time / (n_points - 1)
duty_cycles = []
for i in range(n_points):
    t = i * dt
    x = xmax * (t / default_time)  # map time to angle (assuming linear speed)
    y = xmax * math.sin((0.5*x*math.pi)/(0.5*xmax) - 0.5 * math.pi) + xmax  # compute duty cycle using given function
    duty_cycles.append(y / xmax)  # normalize to range 0 to 1

# compute time to move from 0 to 180 degrees using computed duty cycles
total_time = 0
for i in range(n_points - 1):
    dc1 = duty_cycles[i]
    dc2 = duty_cycles[i + 1]
    dc_avg = (dc1 + dc2) / 2
    dc_time = (dc2 - dc1) / dc_avg * default_time * angle_increment / xmax
    total_time += dc_time

print("Time to move from 0 to 180 degrees using smoothed PWM signal: {:.3f} seconds".format(total_time))