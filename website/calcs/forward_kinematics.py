import numpy as np

def dh_transform(a, alpha, d, theta):
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

def forward_kinematics(theta0, theta1, theta2, theta3, L1=120, L2=88, L3=180):
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

    x, y, z = T[:3, 3]

    return np.array([x, y, z])





