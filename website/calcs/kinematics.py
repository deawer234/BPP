"""
Module for calculation of kinematics for robotic arm.

Author: Daniel Němec
Date: 15.03.2023

Python Version: 3.8.10
"""

import numpy as np

# Computation of the inverse kinematics function according to the doc
def inverse_kinematics(x, y, z, angles, L1=120, L2=88, L3=180):
    r1 = np.sqrt(x**2 + y**2)

    base_angle = np.degrees(np.arctan2(y, x))
    # Limits of the base angle
    if base_angle < 0 or base_angle > 180:
        return None
    
    solutions = []
    
    for i in range(2):
        for angle in np.arange(0, 360, 0.2):
            angle_rad = np.radians(angle)

            Wx = r1 - (L3 * np.cos(angle_rad))
            Wy = z - (L3 * np.sin(angle_rad))

            c2 = (Wx**2 + Wy**2 - L1**2 - L2**2) / (2 * L1 * L2)
            if c2 < -1 or c2 > 1:
                continue

            if i == 0:
                s2 = np.negative(np.sqrt(1 - c2**2))
            else:
                s2 = np.sqrt(1 - c2**2)

            elbow_angle_rad = np.arctan2(s2, c2)
            elbow_angle = np.degrees(elbow_angle_rad)

            # Limits of the elbow angle
            if elbow_angle < -121 or elbow_angle > 59:
                continue

            s1 = ((L1 + L2 * np.cos(elbow_angle_rad)) * Wy - L2 * np.sin(elbow_angle_rad) * Wx) / (Wx**2 + Wy**2)
            c1 = ((L1 + L2 * np.cos(elbow_angle_rad)) * Wx + L2 * np.sin(elbow_angle_rad) * Wy) / (Wx**2 + Wy**2)

            shoulder_angle = np.degrees(np.arctan2(s1, c1))

            # Limits of the shoulder angle
            if shoulder_angle < -24 or shoulder_angle > 156:
                continue

            wrist_angle = angle - elbow_angle - shoulder_angle

            # Limits of the wrist angle
            if wrist_angle >= 245:
                wrist_angle = wrist_angle - 360

            if wrist_angle < -115 or wrist_angle > 65:
                continue

            solutions.append({'base': float(base_angle), 'shoulder': float(shoulder_angle),'elbow': float(elbow_angle),'wrist': float(wrist_angle), 'wrist_rot': angles['wrist_rot'], 'gripper': angles['gripper']})
        
        if solutions:
            break

    # Choosing the best candidate from all the angles
    if solutions:
        min_diff = float('inf')
        best_solution = None

        for solution in solutions:
            diff = sum(abs(angles[key] - solution[key]) for key in ['base', 'shoulder', 'elbow', 'wrist'])
            if diff < min_diff:
                min_diff = diff
                best_solution = solution
        return best_solution
    else:
        return None

# Denavit-Hartenberg transform matrix   
def dh_transform(a, alpha, d, theta):
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

# Computation of the forward kinematics with DH conception
def forward_kinematics(theta0, theta1, theta2, theta3, L1=120, L2=88, L3=180):
    theta0 = np.radians(theta0)
    theta1 = np.radians(theta1)
    theta2 = np.radians(theta2)
    theta3 = np.radians(theta3)

    dh_params = [
        [0, np.pi/2, 0, theta0],
        [L1, 0, 0, theta1],
        [L2, 0, 0, theta2],
        [L3, 0, 0, theta3]
    ]

    transforms = [dh_transform(*params) for params in dh_params]

    T = np.identity(4)
    for transform in transforms:
        T = T @ transform

    x, y, z = np.round(T[:3, 3])

    return np.array([x, y, z])
