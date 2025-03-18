import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np


def init_robot(grip_pressure: float) -> InterbotixManipulatorXS:
    """
    Create an InterbotixManipulatorXS object and set a starting grip pressure.
    Return the robot object for manipulation.
    """
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
            robot_model='px150',
            group_name='arm',
            gripper_name='gripper',
        )

    # starts up the robot, leave 
    bot.gripper.set_pressure(grip_pressure)
    robot_startup()
    return bot

def robot_draw_lines(robot: InterbotixManipulatorXS, robot_base_frame: list[float], canvas_base_frame: list[float], points_list: list[tuple[list[float], list[float]]]) -> list[bool]:
    """
    Using the provided robot arm _robot_ object, draw lines from the given start and end points of each item in points_list. Translate these points from the canvas (whiteboard or paper)
    frame they are given in to the provided base frame of the robot.
    Params:
        - robot: an initialized and started object representing an interbotix PX150 arm.
        - robot_base_frame: the coordinates of the robot's base frame, usually 0,0,0. Given in meters.
        - canvas_base_frame: the coordinates of the canvas the robot is drawing on, with respect to the robot_base_frame. Given in meters.
        - points_list: a list of (point, point) tuples representing the start and end points of a set of lines to be drawn. Given in meters.

    Return: a list of booleans representing the success or failure of each line drawing. Each line specified in _points_list_ will be True if the line was able to be drawn and False if the
    robot was unable to compute a successful transform for the line.
    """
    

    return [False] # TODO

def shutdown_bot(robot: InterbotixManipulatorXS) -> None:
    """
    Shuts down the robot by sending the robot back to the sleep pose and 
    running a shutdown function for the ROS API.
    """
    robot.arm.go_to_sleep_pose()
    robot_shutdown()


if __name__ == '__main__':
    """
    NOTE: much of this code is stubbed out and intended to be filled out as the team progresses making the robot work.
    Specifically, both the ROBOT_BASE_FRAME_XYZ and CANVAS_BASE_FRAME_XYZ values are set at defaults right now and will need
    configured every time the robot and canvas are set up.

    All coordinate and movement values for the robot are in meters (unless otherwise specified).
    """


    # Constant definitions:
    # this value should range from [0, 1]
    GRIP_PRESSURE = 0.25
    assert 0 <= GRIP_PRESSURE and GRIP_PRESSURE <= 1
    # the coordinates of the robot's base frame, known in the docs as the "Space Frame"
    # see: https://docs.trossenrobotics.com/interbotix_xsarms_docs/python_ros_interface.html

    # TODO: both of these are stubbed out and meaningless at the moment
    ROBOT_BASE_FRAME_XYZ = [0,0,0]
    # the coordinates of the bottom left corner of the space the robot is drawing in, with respect to the ROBOT_BASE_FRAME
    CANVAS_BASE_FRAME_XYZ = [0,0,0]
    

    # startup/init the robot
    robot = init_robot(GRIP_PRESSURE)

    # Draw some lines using each set of points:
    # each element of the list is a 2-item tuple representing the start and end points of a line to be drawn by the robot.
    # These points should be with respect to the CANVAS_BASE_FRAME.
    list_of_points: list[tuple[list, list]] = [
        ([0.2, 0, 0.2], [0.6, 0, 0.2]),
    ]

    # draw the lines specified in list_of_points, return a list of how many lines succeeded
    draw_successes = robot_draw_lines(robot, ROBOT_BASE_FRAME_XYZ, CANVAS_BASE_FRAME_XYZ, list_of_points)

    # cleanup
    shutdown_bot(robot)

