import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np
from scale_points import load_waypoints


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
