import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or Qt5Agg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pi, atan2, acos
# Define the kinematic structure of the robot
L1 = 120
L2 = 88
L3 = 145


def forward_kinematics(base, shoulder, elbow, wrist):
    # Compute the transformation matrix for the base
    T_base = np.array([[np.cos(base), -np.sin(base), 0, 0],
                       [np.sin(base), np.cos(base), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
    
    # Compute the transformation matrix for the shoulder
    T_shoulder = np.array([[np.cos(shoulder), -np.sin(shoulder), 0, 0],
                           [0, 0, -1, -L1],
                           [np.sin(shoulder), np.cos(shoulder), 0, 0],
                           [0, 0, 0, 1]])
    
    # Compute the transformation matrix for the elbow
    T_elbow = np.array([[np.cos(elbow), -np.sin(elbow), 0, L2],
                        [0, 0, 1, 0],
                        [-np.sin(elbow), -np.cos(elbow), 0, 0],
                        [0, 0, 0, 1]])
    
    # Compute the transformation matrix for the wrist
    T_wrist = np.array([[np.cos(wrist), -np.sin(wrist), 0, L3],
                        [0, 0, -1, 0],
                        [np.sin(wrist), np.cos(wrist), 0, 0],
                        [0, 0, 0, 1]])
    
    # Compute the end-effector position
    T = T_base @ T_shoulder @ T_elbow @ T_wrist
    end_effector_position = T[:3, 3]
    
    return end_effector_position

# Define the robot arm lengths
# Define the inverse kinematics function


# Define the inverse kinematics function
theta1_min = 0
theta2_min = 24 * pi / 180
theta3_min = 59 * pi / 180
theta4_min = -90 * pi / 180

def inverse_kinematics(x, y, z):
    # Calculate the base angle
    theta1 = atan2(y, x)

    # Calculate the position of the wrist
    wrist_x = x - L3 * np.cos(theta1)
    wrist_y = y - L3 * np.sin(theta1)
    wrist_z = z - L1

    # Calculate the angle between the shoulder and the wrist
    D = (wrist_x ** 2 + wrist_y ** 2 + wrist_z ** 2 - L2 ** 2 - L3 ** 2) / (2 * L2 * L3)
    theta3 = acos(D)

    # Calculate the angle between the ground and the shoulder-wrist line
    alpha = atan2(wrist_z, np.sqrt(wrist_x ** 2 + wrist_y ** 2))

    # Calculate the angle of the shoulder
    theta2 = alpha + atan2(L3 * np.sin(theta3), L2 + L3 * np.cos(theta3))

    # Calculate the angle of the elbow
    theta4 = atan2(-wrist_y*np.cos(theta1)+wrist_x*np.sin(theta1), wrist_x*np.cos(theta1)+wrist_y*np.sin(theta1))-theta2-pi

    # Check if the angles are within the limits
    if (theta1 < 0 or theta1 >= 2*pi or 
        theta2 < theta2_min or theta2 >= (180 - theta3_min) * pi / 180 or 
        theta3 < theta3_min or theta3 >= (180 - theta2_min) * pi / 180 or
        theta4 < theta4_min or theta4 >= 90 * pi / 180):
        return None

    return [theta1, theta2, theta3, theta4]
#sGenerate a grid of points in the workspace
# base_range = np.linspace(-np.pi, np.pi, 25)
# shoulder_range = np.linspace(-np.pi/2, np.pi/2, 5)
# elbow_range = np.linspace(0, np.pi, 5)
# wrist_range = np.linspace(-np.pi/2, np.pi/2, 5)

# # Create a grid of joint angles
# base, shoulder, elbow, wrist = np.meshgrid(base_range, shoulder_range, elbow_range, wrist_range, indexing='ij')

# # Compute the end-effector position for each joint angle
# x = np.zeros_like(base)
# y = np.zeros_like(base)
# z = np.zeros_like(base)
# for i in range(base.shape[0]):
#     for j in range(base.shape[1]):
#         for k in range(base.shape[2]):
#             for l in range(base.shape[3]):
#                 position = forward_kinematics(base[i,j,k,l], shoulder[i,j,k,l], elbow[i,j,k,l], wrist[i,j,k,l])
#                 x[i,j,k,l] = position[0]
#                 y[i,j,k,l] = position[1]
#                 z[i,j,k,l] = position[2] + L1

# # Create a 3D plot of the work envelope
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlim([-0.3, 0.3])
# ax.set_ylim([-0.3, 0.3])
# ax.set_zlim([0, 0.4])
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.scatter(x.flatten(), y.flatten(), z.flatten(), alpha=0.05)
# plt.show()