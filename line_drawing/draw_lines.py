# Robot-specific imports
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS

# Others
import numpy as np
import time
from scale_points import load_waypoints, convert_to_robot_coords
from move_to_waypoints import is_horizontal, compute_adjustments, is_vertical, compute_adjustments_z


# # CONSTANT DEFINITIONS:
# from scale_points import (
#     PAPER_WIDTH,
#     PAPER_HEIGHT,
#     # the bottom left corner of the paper and it's absolute position in the robot's coordinate frame (and it's origin)
#     LEFT_PAPER_CORNER_ABS,
#     # this is the wrong place for these constants, but makes import issues easier for now
#     PAPER_HOVER,
#     PEN_DISPLACEMENT,
# )
# # The distance above the paper to hover before pusing the pen down
# # PAPER_HOVER = 0.15
# # Robot values:
# GRIPPER_PRESSURE = 1.0
# SLEEP_TIME = 3.0
# TRAJECTORY_TIME = 1.2
# ACCEL_TIME = TRAJECTORY_TIME/5
# # Other:
# # The z difference from the robot's end effector to the pen tip
# # PEN_DISPLACEMENT = 0.015
from constants import (
    PAPER_HOVER,
    PEN_DISPLACEMENT,
    LEFT_PAPER_CORNER_ABS,
    SLEEP_TIME,
    TRAJECTORY_TIME,
    ACCEL_TIME,
    PAPER_HEIGHT,
    PAPER_WIDTH,
    GRIPPER_PRESSURE,
)



# HELPER FUNCS:
def get_eff_coords(robot: InterbotixManipulatorXS) -> np.ndarray:
    """
    Gets the x, y, z coordinates of the robot's end effector as a numpy array.
    """
    ee_pose = robot.arm.get_ee_pose()
    cur_xyz = np.array(ee_pose)[:-1, -1].T
    return cur_xyz

def pen_to_paper(robot: InterbotixManipulatorXS, paper_coords: np.ndarray) -> tuple[bool, float]:
    """
    Puts the robot's pen down onto the paper at the current x, y location of the end effector.
    """
    robot.arm.set_trajectory_time(TRAJECTORY_TIME)
    cur_xyz = get_eff_coords(robot)
    print(f"Moving the pen down to the paper at coords: {cur_xyz[0], cur_xyz[1], paper_coords[2] + PEN_DISPLACEMENT}")
    success = robot.arm.set_ee_pose_components(cur_xyz[0], cur_xyz[1], paper_coords[2] + PEN_DISPLACEMENT)[1]
    if success:
        time.sleep(SLEEP_TIME)
    
    return success, get_eff_coords(robot)[2]

def lift_pen(robot: InterbotixManipulatorXS) -> bool:
    """
    Lifts the robot's end effector PAPER_HOVER distance above the paper it is drawing on.
    """
    robot.arm.set_trajectory_time(TRAJECTORY_TIME)
    cur_xyz = get_eff_coords(robot)
    print(f"Attempting to lift the pen up to: {cur_xyz[0], cur_xyz[1], LEFT_PAPER_CORNER_ABS[2] + PAPER_HOVER}")
    success = robot.arm.set_ee_pose_components(cur_xyz[0], cur_xyz[1], LEFT_PAPER_CORNER_ABS[2] + PAPER_HOVER)[1]
    if success:
        time.sleep(SLEEP_TIME)

    return success


# The main function
def draw_lines():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
        robot_model='rx200',
        group_name='arm',
        gripper_name='gripper',
    )
    
    # init the robot, set some values
    robot_startup()
    bot.arm.set_trajectory_time(TRAJECTORY_TIME)
    bot.gripper.set_pressure(GRIPPER_PRESSURE)
    
    # go to the default home pose and grab the marker
    bot.arm.go_to_home_pose()
    time.sleep(SLEEP_TIME)
    print(f"Took bot to home pose, absolute position: {get_eff_coords(bot)}")
    print(f"Waiting {SLEEP_TIME} seconds to grab pen")
    bot.gripper.release()
    time.sleep(SLEEP_TIME)
    bot.gripper.grasp()

    # get a list of lines to draw, in robot's scaled coordinates w.r.t to the corner of the paper
    # ie. the bottom left corner of the paper is (0, 0) and the top right is (+Width, +Height), but 
    # in the scale of the coordinates passed to set_ee_pose_components()
    lines = load_waypoints()
    print("Loaded lines to draw")
    """  
    In the ROBOT's coordinate frame:

            + X
            
      + Y   Paper  - Y
            here     
    
            ROBOT
    
            - X
    """ 
    # the final list of lines to draw, with respect to the base frame of the robot, scaled with the proper coords
    lines = convert_to_robot_coords(lines)
    print("Converted lines in paper's coordinate frame to the robot's coordinate frame")

    # actually draw each line
    for line in lines:
        # These lines are in the coordiante frame of the robot
        start = np.array([line[0], line[1], LEFT_PAPER_CORNER_ABS[2]])
        end = np.array([line[2], line[3], LEFT_PAPER_CORNER_ABS[2]])

        if (start[0] < end[0]):
            start, end = end, start
        x0, x1 = start[0], end[0]
        y0, y1 = start[1], end[1]

        # move ABOVE the starting position
        paper_hover_dist = LEFT_PAPER_CORNER_ABS[2] + PAPER_HOVER
        print(f"Moving above the first point of the line at {start[0], start[1], paper_hover_dist}")
        bot.arm.set_ee_pose_components(start[0], start[1], paper_hover_dist, moving_time=TRAJECTORY_TIME, accel_time=ACCEL_TIME)
        time.sleep(SLEEP_TIME)

        # put the writing implement in contact with the paper, get the actual z location of the pen when it touches the paper
        actual_z = pen_to_paper(bot, LEFT_PAPER_CORNER_ABS)[1]

        # move to the end of the line
        if is_horizontal(start[0], end[0]):
            # do waypoints
            print("Found Horizontal Line")
            num_waypoints = 10 #(min 2)amnt of waypoints we manually generate
            x_points = np.linspace(x0, x1, num=num_waypoints)
            y_points = np.linspace(y0, y1, num=num_waypoints)

            # For a horizontal line we only need to z-adjust once because the x coords are not changing
            z_adjust = compute_adjustments_z(start[0], x_min=LEFT_PAPER_CORNER_ABS[0] - PAPER_HEIGHT, x_max=LEFT_PAPER_CORNER_ABS[0])
            # Interate through intermediate waypoints
            for x, y in zip(x_points[1:], y_points[1:]):
                x_adjust = compute_adjustments(y, y_max=LEFT_PAPER_CORNER_ABS[1], y_min=LEFT_PAPER_CORNER_ABS[1] - PAPER_WIDTH)
                print(f"Waypoint: {x + x_adjust, y, actual_z + z_adjust}")
                if not bot.arm.set_ee_pose_components(
                        x=x + x_adjust, y=y, z=actual_z + z_adjust, 
                        blocking=False, moving_time=TRAJECTORY_TIME/num_waypoints, accel_time=ACCEL_TIME, 
                        custom_guess=bot.arm.get_joint_positions()
                    )[1]:
                    # if one waypoint fails, don't execute more
                    print(f"Waypoint {list(x_points).index(x) - 1} failed, skipping rest")
                    break
                time.sleep(SLEEP_TIME/num_waypoints)
            print(f"Moved to end point: {x0, y0}")
        elif is_vertical:
            z_adjust = compute_adjustments_z(end[0], x_min=LEFT_PAPER_CORNER_ABS[0] - PAPER_HEIGHT, x_max=LEFT_PAPER_CORNER_ABS[0])
            print("Found Vertical Line")
            success = bot.arm.set_ee_pose_components(end[0], end[1], actual_z + z_adjust, moving_time=TRAJECTORY_TIME, accel_time=ACCEL_TIME)[1]
            if success:
                time.sleep(SLEEP_TIME)       
        else:
            # move to the second point on the line
            print(f"Moving to the second point on the line: {end[0], end[1], actual_z}")
            success = bot.arm.set_ee_pose_components(
                    x=end[0], y=end[1], z=actual_z, 
                    moving_time=TRAJECTORY_TIME, accel_time=ACCEL_TIME,
                    custom_guess=bot.arm.get_joint_positions()
                )[1]
            if success:
                time.sleep(SLEEP_TIME)
    
        # pick the pen back up to get ready for the next drawing
        lift_pen(bot)

    # clean up after drawing lines
    bot.arm.set_trajectory_time(TRAJECTORY_TIME)
    print("Stopping up and going home")
    bot.arm.go_to_home_pose()
    time.sleep(SLEEP_TIME)
    bot.gripper.release()
    bot.arm.go_to_sleep_pose()
    time.sleep(SLEEP_TIME)
    print("Shutting down")
    robot_shutdown()

if __name__ == "__main__":
    draw_lines()