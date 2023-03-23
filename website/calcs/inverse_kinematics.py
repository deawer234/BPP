import numpy as np
from scipy.optimize import minimize

# Define the kinematic structure of the robot
L1 = 1.0
L2 = 0.8
L3 = 0.5

# Define the forward kinematics function
def forward_kinematics(q):
    x = L1*np.cos(q[0]) + L2*np.cos(q[0]+q[1]) + L3*np.cos(q[0]+q[1]+q[2])
    y = L1*np.sin(q[0]) + L2*np.sin(q[0]+q[1]) + L3*np.sin(q[0]+q[1]+q[2])
    return np.array([x, y])

# Define the inverse kinematics function
def inverse_kinematics(x_desired, y_desired):
    q = np.array([0.0, 0.0, 0.0]) # Initial guess for joint angles
    x_actual, y_actual = forward_kinematics(q)
    error = np.sqrt((x_actual-x_desired)**2 + (y_actual-y_desired)**2) # Euclidean distance error
    while error > 1e-6:
        J = jacobian(q)
        J_T = J.T
        delta_q = np.dot(J_T, np.array([x_desired-x_actual, y_desired-y_actual]))
        q = q + delta_q
        x_actual, y_actual = forward_kinematics(q)
        error = np.sqrt((x_actual-x_desired)**2 + (y_actual-y_desired)**2)
    return q

# Define the Jacobian function
def jacobian(q):
    eps = 1e-6
    J = np.zeros((2,3))
    for i in range(3):
        q_plus = np.copy(q)
        q_plus[i] += eps
        x_plus, y_plus = forward_kinematics(q_plus)
        x_minus, y_minus = forward_kinematics(q)
        J[0,i] = (x_plus - x_minus) / eps
        J[1,i] = (y_plus - y_minus) / eps
    return J

# Test the inverse kinematics function
x_desired = 1.5
y_desired = 1.0
q = inverse_kinematics(x_desired, y_desired)
print("Joint angles required to reach (", x_desired, ",", y_desired, "): ", q)