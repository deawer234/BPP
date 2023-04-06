import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def plot_top_view(z, x, base_angle, L1=120, L2=88, L3=124):
    circle = Circle((0, 0), L1 + L2 + L3, color='gray', alpha=0.2)
    plt.gca().add_patch(circle)

    plt.plot([0, z], [0, x], marker='o', linestyle='-')
    plt.annotate(f"Base angle: {base_angle:.2f}°", xy=(z, x), xytext=(z + 10, x + 10),
                 arrowprops=dict(arrowstyle="->"))

    plt.axis('equal')
    plt.xlabel('Z')
    plt.ylabel('X')
    plt.title('Top View - Base Rotation')


def inverse_kinematics(x, y, z, L1=120, L2=88, L3=124):
    base_angle = np.degrees(np.arctan2(y, x))
    print("Base angle:", base_angle)

    # Calculate the distance from the base to the target point in the XY plane
    r = np.sqrt(x**2 + y**2)

    # Project the target point into the 2D plane (perpendicular to the base rotation axis)
    x_proj = r - (L3 * np.cos(np.radians(base_angle)))
    y_proj = z - (L3 * np.sin(np.radians(base_angle)))

    for angle in range(0, 360, 1):
        angle_rad = np.radians(angle)
        Wx = x_proj - (L3 * np.cos(angle_rad))
        Wy = y_proj - (L3 * np.sin(angle_rad))
        c2 = (Wx**2 + Wy**2 - L1**2 - L2**2) / (2 * L1 * L2)
        if c2 < -1 or c2 > 1:
            continue

        s2 = np.negative(np.sqrt(1 - c2**2))

        elbow_angle_rad = np.arctan2(s2, c2)
        elbow_angle = np.degrees(elbow_angle_rad)

        if elbow_angle < -121 or elbow_angle > 59:
            continue

        s1 = ((L1 + L2 * np.cos(elbow_angle_rad)) * Wy - L2 * np.sin(elbow_angle_rad) * Wx) / (Wx**2 + Wy**2)
        c1 = ((L1 + L2 * np.cos(elbow_angle_rad)) * Wx + L2 * np.sin(elbow_angle_rad) * Wy) / (Wx**2 + Wy**2)

        shoulder_angle = np.degrees(np.arctan2(s1, c1))

        if shoulder_angle < -24 or shoulder_angle > 156:
            continue

        wrist_angle = angle - elbow_angle - shoulder_angle
        if wrist_angle > 90:
            wrist_angle = wrist_angle - 360

        if wrist_angle < -90 or wrist_angle > 90:
            continue
        ex = L1 * np.cos(np.radians(shoulder_angle))
        ey = L1 * np.sin(np.radians(shoulder_angle))

        wx = ex + L2 * np.cos(np.radians(shoulder_angle + elbow_angle))
        wy = ey + L2 * np.sin(np.radians(shoulder_angle + elbow_angle))
        plt.figure()
        plt.plot([0, ex, wx, x], [0, ey, wy, y], marker="o")
        plt.text(x, y, f"{angle}°")
        plt.xlim(-350, 350)
        plt.ylim(-350, 350)
        plt.gca().set_aspect("equal", adjustable="box")
        break;

    
    plt.title("Side View")
    circle = Circle((0, 0), 120 + 88 + 124, color='gray', alpha=0.2)
    plt.gca().add_patch(circle)
    plt.grid(True)
    plt.title("Inverse Kinematics Visualization")
    plt.figure()
    plot_top_view(z, x, base_angle, L1, L2, L3)
    plt.show()
# def inverse_kinematics(x, y, z, L1=120, L2=88, L3=124):
#     r = np.sqrt(x**2 + y**2)
    
#     # Calculate the position of the wrist relative to the shoulder joint
#     Wx = r - L3
#     Wy = y

#     D = np.sqrt(Wx**2 + Wy**2)
    
#     # Check if the target is within reach
#     reachable = D <= (L1 + L2)

#     if not reachable:
#         raise ValueError("Target is not reachable")

#     # Calculate the joint angles
#     theta0 = np.degrees(np.arctan2(z, x))
#     theta1 = np.degrees(np.arctan2(Wy, Wx) - np.arccos((D**2 + L1**2 - L2**2) / (2 * L1 * D)))
#     theta2 = np.degrees(np.arccos((L1**2 + L2**2 - D**2) / (2 * L1 * L2)) - np.pi)
#     theta3 = 180 + theta1 + theta2

#     return theta0, theta1, theta2, theta3
# Test the function
# x, y, z = 200, 100, 0
# L1, L2, L3 = 120, 88, 124
# theta0, theta1, theta2, theta3 = inverse_kinematics(x, y, z, L1, L2, L3)
# print("Joint angles (degrees):", theta0, theta1, theta2, theta3)


# import math
# import numpy as np

# # Arm dimensions
# a1 = 0      # Base
# a2 = 120    # Shoulder length
# a3 = 88     # Elbow length
# a4 = 124    # Wrist + Rotator + End effector combined length

# def check_joint_limits(joint_angles_degrees):
#     joint_limits_degrees = [
#         (0, 360),  # Base rotation
#         (24, 204),  # Shoulder
#         (59, 239),  # Elbow
#         (90, 270),  # Wrist
#         (0, 360),  # Wrist rotation
#         # No limits provided for the gripper
#     ]

#     for i, (angle, limits) in enumerate(zip(joint_angles_degrees, joint_limits_degrees)):
#         if not limits[0] <= angle <= limits[1]:
#             print(f"Joint {i + 1} angle {angle} is out of limits {limits}")
#             return False
#     return True

# def inverse_kinematics(target_position, target_orientation):
#     x, y, z = target_position
#     alpha, beta, gamma = target_orientation

#     # Joint 1 (Base rotation)
#     theta1 = math.atan2(y, x)

#     # Calculate the wrist center position
#     r = math.sqrt(x**2 + y**2)
#     h = z - a1

#     # Joint 2 (Shoulder) and Joint 3 (Elbow)
#     A = a3
#     B = a4
#     C = math.sqrt(h**2 + (r - a2)**2)

#     # Calculate angles using the law of cosines
#     angle_a = math.acos((B**2 + C**2 - A**2) / (2 * B * C))
#     angle_b = math.acos((A**2 + C**2 - B**2) / (2 * A * C))
#     angle_c = math.acos((A**2 + B**2 - C**2) / (2 * A * B))

#     # Calculate the shoulder and elbow angles
#     theta2 = math.atan2(h, r - a2) - angle_a
#     theta3 = math.pi - angle_c

#     # Calculate wrist angles (theta4, theta5, theta6) based on target orientation
#     # Euler angles (alpha, beta, gamma) are used for simplicity
#     theta4 = alpha - theta2 - theta3
#     theta5 = beta
#     theta6 = gamma

#     # Convert radians to degrees
#     joint_angles = [theta1, theta2, theta3, theta4, theta5, theta6]
#     joint_angles_degrees = [math.degrees(angle) for angle in joint_angles]

#     return joint_angles_degrees
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
