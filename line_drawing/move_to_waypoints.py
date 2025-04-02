import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np
from scale_points import load_waypoints


# def move(absolute=False, **kwargs):
#     """
#     Move the end-effector using either relative Cartesian trajectory or absolute pose components.

#     Args:
#         absolute (bool): If True, use absolute pose via set_ee_pose_components.
#                         If False (default), use relative motion via set_ee_cartesian_trajectory.
#         **kwargs: x, y, z, roll, pitch, yaw (any subset, depending on function used).
#     """
#     if absolute:
#         success = bot.arm.set_ee_pose_components(**kwargs)
#     else:
#         #doing this to the trajectory as we only want a singular waypoint (strict path planning)
#         move_time=1.0 #seconds
#         success = bot.arm.set_ee_cartesian_trajectory(moving_time=move_time,
#             wp_moving_time=move_time,
#             wp_accel_time=(move_time/2),
#             wp_period=move_time,
#             **kwargs)

#     if success:
#         method = "absolute pose" if absolute else "relative trajectory"
#         desc = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
#         # print(f"Moved using {method}: {desc}")
#     else:
#         print(f"Failed to move with args: {kwargs}")

#     time.sleep(sleep_time)
#     print("Sleep done")


def compute_adjustments(y, y_min, y_max):
    """
    Compute the x adjustments based on the position in the xy-plane. Smoothing based on
    the natural curvature of the robot while making a change in the y-axis.

    Args:
    y (float): The y coordinate.
    y_min (float): Min y coordinate
    y_max (float): Max y coordinate

    Returns:
        float: Adjustment in the x-axis
    """
    # Scaling factor
    k_x = 0.01

    y_factor = (y - y_min) / (y_max - y_min) * 2 - 1  # Maps y in [-0.1, 0.1] to [-1, 1]

    # Compute y adjustment based on x movement (higher at min/max x)
    x_adjustment = -k_x * (1 - abs(y_factor))  # Maximum boost near x_min/x_max

    return x_adjustment

def compute_adjustments_z(x, x_min, x_max):
    """
    Compute the z adjustments based on the position in the xy-plane. Smoothing based on
    the natural weight of the robot while making a change in the x-axis.

    Args:
    x (float): The x coordinate.
    x_min (float): Min x coordinate.
    x_max (float): Max x coordinate.

    Returns:
        float: Adjustment in the z-axis
    """

    # Scaling factor
    k_z = 0.002

    x_factor = (x - x_min) / (x_max - x_min)  # Maps x in [0.2, 0.35] to [0, 1]

    # Compute z adjustment based on y movement
    z_adjustment = -k_z * (1 - x_factor)


    return z_adjustment

def is_horizontal(x0, x1):
    """
    Determines if the line is a horizontal 
    or less than 3% change on the x-axis based on the robot coords

    Args:
    x0 - initial x value in the line
    x1 - last x value in the line

    Returns:
    True if horizontal otherwise False
    """
    return abs(x1 - x0) < 0.03  

def is_vertical(y0, y1):
    """
    Determines if the line is a vertical 
    or less than 3% change on the y-axis based on the robot coords

    Args:
    y0 - initial y value in the line
    y1 - last y value in the line

    Returns:
    True if vertical otherwise False
    """
    return abs(y1 - y0) < 0.03  

# # starts up the robot, leave 
# bot.gripper.set_pressure(2.0)
# robot_startup()

# # some sample moving code
# bot.arm.go_to_home_pose()
# time.sleep(2)
# print("At home pose")

# bot.gripper.release()
# print('Put marker in the gripper')
# time.sleep(4)
# bot.gripper.grasp()
# time.sleep(2)

# waypoints = load_waypoints()
# print(waypoints)
# z_const = 0.1

# for segment in waypoints:
#     x0, y0, x1, y1 = segment
#     # Move to initial point on the line
#     move(x=x1, z=z_const, y=y1, blocking=False, absolute=True)
#     print(f"Moved to initial point: {x1, y1}")

#     if is_horizontal(x0, x1):
#         print("Found Horizontal Line")
#         num_waypoints = 5 #(min 2)amnt of waypoints we manually generate
#         x_points = np.linspace(x0, x1, num=num_waypoints)
#         y_points = np.linspace(y0, y1, num=num_waypoints)

#         # Interate through intermediate waypoints
#         for x, y in zip(x_points[num_waypoints - 1::-1], y_points[num_waypoints - 1::-1]):
#             x_adjust = compute_adjustments(x, y)
#             print(f"Waypoint: {x+x_adjust,y, z_const}")
#             move(x=x + x_adjust, z=z_const, y=y, blocking=False, absolute=True)
#         print(f"Moved to end point: {x0, y0}")
#     else:
#         # TODO: Add the code for a normal move between points
#         move(x=x0, z=z_const, y=y1, blocking=False, absolute=True)

