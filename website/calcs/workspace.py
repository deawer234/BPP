from vpython import *

# Define robotic arm dimensions
SHOULDER_LEN = 120
ELBOW_LEN = 88
WRIST_LEN = 124

# Define initial end effector position and joint angles
x, y, z = 211, 35, 50
theta1, theta2, theta3, theta4 = [9.42, 4.86, 111.83, -70.17]

# Compute joint positions based on joint angles
base_pos = vector(0, 0, 0)
shoulder_pos = base_pos + vector(SHOULDER_LEN*cos(radians(theta1)), SHOULDER_LEN*sin(radians(theta1)), 0)
elbow_pos = shoulder_pos + vector(ELBOW_LEN*cos(radians(theta2)), ELBOW_LEN*sin(radians(theta2)), 0)
wrist_pos = elbow_pos + vector(WRIST_LEN*cos(radians(theta2+theta3)), WRIST_LEN*sin(radians(theta2+theta3)), z)

# Create arm segments and joints
base = sphere(pos=base_pos, radius=10, color=color.red)
rate(1)
shoulder = sphere(pos=shoulder_pos, radius=10, color=color.green)
rate(1)
upper_arm = cylinder(pos=shoulder_pos, axis=elbow_pos-shoulder_pos, radius=5, color=color.green)
rate(1)
elbow = sphere(pos=elbow_pos, radius=10, color=color.blue)
rate(1)
forearm = cylinder(pos=elbow_pos, axis=wrist_pos-elbow_pos, radius=5, color=color.blue)
rate(1)
wrist = sphere(pos=wrist_pos, radius=10, color=color.yellow)
rate(1)

# Animate arm motion
while True:
    rate(30)
    
    # Update joint angles
    theta1 += 1
    theta2 += 1
    theta3 += 1
    theta4 += 1
    
    # Compute joint positions based on joint angles
    shoulder_pos = base_pos + vector(SHOULDER_LEN*cos(radians(theta1)), SHOULDER_LEN*sin(radians(theta1)), 0)
    elbow_pos = shoulder_pos + vector(ELBOW_LEN*cos(radians(theta2)), ELBOW_LEN*sin(radians(theta2)), 0)
    wrist_pos = elbow_pos + vector(WRIST_LEN*cos(radians(theta2+theta3)), WRIST_LEN*sin(radians(theta2+theta3)), z)
    
    # Update arm segments and joints
    shoulder.pos = shoulder_pos
    upper_arm.axis = elbow_pos - shoulder_pos
    elbow.pos = elbow_pos
    forearm.pos = elbow_pos
    forearm.axis = wrist_pos - elbow_pos
    wrist.pos = wrist_pos