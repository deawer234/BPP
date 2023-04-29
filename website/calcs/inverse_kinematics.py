import numpy as np
from scipy.optimize import minimize
from website.calcs.forward_kinematics import forward_kinematics


def inverse_kinematics(x, y, z, angles, L1=120, L2=88, L3=180):
    r1 = np.sqrt(x**2 + y**2)
    # Calculate the base angle
    base_angle = np.degrees(np.arctan2(y, x))
    #print(base_angle)
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
                    
            if elbow_angle < -121 or elbow_angle > 59:
                continue

            s1 = ((L1 + L2 * np.cos(elbow_angle_rad)) * Wy - L2 * np.sin(elbow_angle_rad) * Wx) / (Wx**2 + Wy**2)
            c1 = ((L1 + L2 * np.cos(elbow_angle_rad)) * Wx + L2 * np.sin(elbow_angle_rad) * Wy) / (Wx**2 + Wy**2)

            shoulder_angle = np.degrees(np.arctan2(s1, c1))
            
            if shoulder_angle < -24 or shoulder_angle > 156:
                continue

            wrist_angle = angle - elbow_angle - shoulder_angle

            #print(str(wrist_angle) +"  " + str(wrist_angle - 360))
            if wrist_angle >= 245:
                wrist_angle = wrist_angle - 360

            if wrist_angle < -115 or wrist_angle > 65:
                continue
            #print(angles)
            solutions.append({'base': float(base_angle), 'shoulder': float(shoulder_angle),'elbow': float(elbow_angle),'wrist': float(wrist_angle), 'wrist_rot': angles['wrist_rot'], 'gripper': angles['gripper']})
        if solutions:
            break
    total_default = 0

    if solutions:
        min_diff = float('inf')
        best_solution = None

        for solution in solutions:
            diff = sum(abs(angles[key] - solution[key]) for key in ['base', 'shoulder', 'elbow', 'wrist'])
            if diff < min_diff:
                min_diff = diff
                best_solution = solution
        print(best_solution)
        return best_solution
    
    else:
        return None

