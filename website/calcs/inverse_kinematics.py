import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D

def plot_arm_3d(x, y, z, L1, L2, L3, angles):
    base_angle, shoulder_angle, elbow_angle, wrist_angle = angles

    # Convert angles to radians
    base_rad = np.radians(base_angle)
    shoulder_rad = np.radians(shoulder_angle)
    elbow_rad = np.radians(elbow_angle)
    wrist_rad = np.radians(wrist_angle)

    # Calculate the joint positions
    x1 = L1 * np.cos(shoulder_rad)
    y1 = L1 * np.sin(shoulder_rad)
    z1 = 0

    x2 = x1 + L2 * np.cos(shoulder_rad + elbow_rad)
    y2 = y1 + L2 * np.sin(shoulder_rad + elbow_rad)
    z2 = 0

    x3 = x2 + L3 * np.cos(shoulder_rad + elbow_rad + wrist_rad)
    y3 = y2 + L3 * np.sin(shoulder_rad + elbow_rad + wrist_rad)
    z3 = z

    # Apply base rotation
    x1_rotated = x1 * np.cos(base_rad) - z1 * np.sin(base_rad)
    z1_rotated = x1 * np.sin(base_rad) + z1 * np.cos(base_rad)

    x2_rotated = x2 * np.cos(base_rad) - z2 * np.sin(base_rad)
    z2_rotated = x2 * np.sin(base_rad) + z2 * np.cos(base_rad)

    x3_rotated = x3 * np.cos(base_rad) - z3 * np.sin(base_rad)
    z3_rotated = x3 * np.sin(base_rad) + z3 * np.cos(base_rad)

    # Plot the arm in 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the links
    ax.plot([0, x1_rotated], [0, y1], [0, z1_rotated], 'b', linewidth=4)
    ax.plot([x1_rotated, x2_rotated], [y1, y2], [z1_rotated, z2_rotated], 'g', linewidth=4)
    ax.plot([x2_rotated, x3_rotated], [y2, y3], [z2_rotated, z3_rotated], 'r', linewidth=4)

    # Plot the joints
    ax.scatter([0, x1_rotated, x2_rotated], [0, y1, y2], [0, z1_rotated, z2_rotated], c='k', s=100)
    ax.scatter([x3_rotated], [y3], [z3_rotated], c='m', s=100, marker='x')

    # Set plot labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set plot limits
    ax.set_xlim([-L1 - L2 - L3, L1 + L2 + L3])
    ax.set_ylim([-L1 - L2 - L3, L1 + L2 + L3])
    ax.set_zlim([0, L1 + L2 + L3])

    # Show the plot
    plt.show()
# Example 


def plot_arm_3ddd(base_angle, shoulder_angle, elbow_angle, wrist_angle, L1=120, L2=88, L3=124):
    base_angle_rad = np.radians(base_angle)
    shoulder_angle_rad = np.radians(shoulder_angle)
    elbow_angle_rad = np.radians(elbow_angle)
    
    # Top-down view (X-Y plane)
    ex = L1 * np.cos(base_angle_rad) * np.cos(shoulder_angle_rad)
    ey = L1 * np.sin(base_angle_rad) * np.cos(shoulder_angle_rad)
    wx = ex + L2 * np.cos(base_angle_rad) * np.cos(shoulder_angle_rad + elbow_angle_rad)
    wy = ey + L2 * np.sin(base_angle_rad) * np.cos(shoulder_angle_rad + elbow_angle_rad)
    tx = wx + L3 * np.cos(base_angle_rad) * np.cos(shoulder_angle_rad + elbow_angle_rad + np.radians(wrist_angle))
    ty = wy + L3 * np.sin(base_angle_rad) * np.cos(shoulder_angle_rad + elbow_angle_rad + np.radians(wrist_angle))

    plt.figure()
    plt.plot([0, ex, wx, tx], [0, ey, wy, ty], marker="o")
    plt.text(tx, ty, f"({tx:.2f}, {ty:.2f})")
    plt.xlim(-350, 350)
    plt.ylim(-350, 350)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.title("Top-down View (X-Y plane)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)

        # Side view (Y-Z plane)
                # ex = L1 * np.cos(np.radians(shoulder_angle))
            # ey = L1 * np.sin(np.radians(shoulder_angle))

            # wx = ex + L2 * np.cos(np.radians(shoulder_angle + elbow_angle))
            # wy = ey + L2 * np.sin(np.radians(shoulder_angle + elbow_angle))
            
            # plt.plot([0, ex, wx, x], [0, ey, wy, y], marker="o")
            # plt.text(x, y, f"{angle}°")
            # plt.xlim(-350, 350)
            # plt.ylim(-350, 350)
            # plt.gca().set_aspect("equal", adjustable="box")
    ez = L1 * np.sin(shoulder_angle_rad)
    wz = ez + L2 * np.sin(shoulder_angle_rad + elbow_angle_rad)
    tz = wz + L3 * np.sin(shoulder_angle_rad + elbow_angle_rad + np.radians(wrist_angle))

    plt.figure()
    plt.plot([0, ey, wy, ty], [0, ez, wz, tz], marker="o")
    plt.text(ty, tz, f"({ty:.2f}, {tz:.2f})")
    plt.xlim(-350, 350)
    plt.ylim(-350, 350)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.title("Side View (Y-Z plane)")
    plt.xlabel("Y")
    plt.ylabel("Z")
    plt.grid(True)

    plt.show()


from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_arm(base_angle, shoulder_angle, elbow_angle, wrist_angle, L1=120, L2=88, L3=124):
    base_angle_rad = np.radians(base_angle)
    shoulder_angle_rad = np.radians(shoulder_angle)
    elbow_angle_rad = np.radians(elbow_angle)
    wrist_angle_rad = np.radians(wrist_angle)

    x1 = L1 * np.cos(shoulder_angle_rad) * np.cos(base_angle_rad)
    y1 = L1 * np.cos(shoulder_angle_rad) * np.sin(base_angle_rad)
    z1 = L1 * np.sin(shoulder_angle_rad)

    x2 = x1 + L2 * np.cos(shoulder_angle_rad + elbow_angle_rad) * np.cos(base_angle_rad)
    y2 = y1 + L2 * np.cos(shoulder_angle_rad + elbow_angle_rad) * np.sin(base_angle_rad)
    z2 = z1 + L2 * np.sin(shoulder_angle_rad + elbow_angle_rad)

    x3 = x2 + L3 * np.cos(shoulder_angle_rad + elbow_angle_rad + wrist_angle_rad) * np.cos(base_angle_rad)
    y3 = y2 + L3 * np.cos(shoulder_angle_rad + elbow_angle_rad + wrist_angle_rad) * np.sin(base_angle_rad)
    z3 = z2 + L3 * np.sin(shoulder_angle_rad + elbow_angle_rad + wrist_angle_rad)

    x = [0, x1, x2, x3]
    y = [0, y1, y2, y3]
    z = [0, z1, z2, z3]

    fig = plt.figure(figsize=(16, 4))

    # Top view
    ax1 = fig.add_subplot(131)
    ax1.plot(x, y, marker='o')
    ax1.scatter(x3, y3, c='r', marker='x', label=f"Target ({x3:.2f}, {y3:.2f})")
    ax1.set_title('Top View')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.axis('equal')
    ax1.legend()

    # Side view
    ax2 = fig.add_subplot(132)
    ax2.plot(x, z, marker='o')
    ax2.scatter(x3, z3, c='r', marker='x', label=f"Target ({x3:.2f}, {z3:.2f})")
    ax2.set_title('Side View')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Z')
    ax2.axis('equal')
    ax2.legend()

    # 3D view
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.plot(x, y, z, marker='o')
    ax3.scatter(x3, y3, z3, c='r', marker='x', label=f"Target ({x3:.2f}, {y3:.2f}, {z3:.2f})")

    # Work envelope sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    sphere_x = (L1 + L2 + L3) * np.outer(np.cos(u), np.sin(v))
    sphere_y = (L1 + L2 + L3) * np.outer(np.sin(u), np.sin(v))
    sphere_z = (L1 + L2 + L3) * np.outer(np.ones(np.size(u)), np.cos(v))
    ax3.plot_surface(sphere_x, sphere_y, sphere_z, color='c', alpha=0.1)

    ax3.set_title('3D View')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.legend()

    plt.show()

# Example usage:

def inverse_kinematics(x, y, z, L1=120, L2=88, L3=124):
    r1 = np.sqrt(x**2 + y**2)
    
    # Calculate the base angle
    base_angle = np.degrees(np.arctan2(y, x))
    print(base_angle)

    solutions = []

    for angle in range(0, 360, 1):
        angle_rad = np.radians(angle)

        Wx = r1 - (L3 * np.cos(angle_rad))
        Wy = z - (L3 * np.sin(angle_rad))

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
        
        solutions.append({'base': int(base_angle), 'shoulder': int(shoulder_angle),'elbow': int(elbow_angle),'wrist': int(wrist_angle), 'wrist_rot': 90, 'gripper': 90})

    if solutions.__len__() == 0:
        return None
    
    #plot_arm(base_angle, shoulder_angle, elbow_angle, wrist_angle)
    return solutions.pop(int(solutions.__len__()/2))


    
