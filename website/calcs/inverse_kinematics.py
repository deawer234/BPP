import klampt
from klampt.model import ik


# import math

# # Arm dimensions (in millimeters)
# SHOULDER_LEN = 120
# ELBOW_LEN = 88
# WRIST_LEN = 124

# # Joint angle limits (in degrees)
# SHOULDER_MIN = 24
# SHOULDER_MAX = 204
# ELBOW_MIN = 59
# ELBOW_MAX = 239
# WRIST_MIN = 90
# WRIST_MAX = 270

# def inverse_kinematics(x, y, z):
#     """Compute inverse kinematics for a 4-DOF robotic arm."""
    
#     # Compute theta1 (base rotation)
#     theta1 = math.atan2(y, x)
    
#     # Compute wrist position in the arm's XY plane
#     r_xy = math.sqrt(x**2 + y**2) - SHOULDER_LEN
#     z_ = z - WRIST_LEN

#     # Compute theta2 (shoulder joint)
#     r = math.sqrt(r_xy**2 + z_**2)
#     s = z_ / r
#     c = r_xy / r
#     alpha = math.acos((SHOULDER_LEN**2 + r**2 - ELBOW_LEN**2) / (2 * SHOULDER_LEN * r))
#     theta2 = math.atan2(s, c) + alpha

#     # Compute theta3 (elbow joint)
#     beta = math.acos((SHOULDER_LEN**2 + ELBOW_LEN**2 - r**2) / (2 * SHOULDER_LEN * ELBOW_LEN))
#     theta3 = math.pi - beta

#     # Compute wrist position in the arm's YZ plane
#     wx__ = x - SHOULDER_LEN * math.cos(theta1) * math.cos(theta2) - ELBOW_LEN * math.cos(theta1) * math.cos(theta2 + theta3)
#     wy__ = y - SHOULDER_LEN * math.sin(theta1) * math.cos(theta2) - ELBOW_LEN * math.sin(theta1) * math.cos(theta2 + theta3)
#     wz__ = z - SHOULDER_LEN * math.sin(theta2) - ELBOW_LEN * math.sin(theta2 + theta3)

#     # Compute theta4 (wrist joint)
#     theta4 = math.atan2(wz__, math.sqrt(wx__**2 + wy__**2)) - math.atan2(WRIST_LEN * math.sin(theta2 + theta3), SHOULDER_LEN + ELBOW_LEN * math.cos(theta2 + theta3))

#     return [math.degrees(theta1), math.degrees(theta2), math.degrees(theta3),
#             math.degrees(theta4)]