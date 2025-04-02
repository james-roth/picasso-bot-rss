# The purpose of this file is to have the robot move its' end effector to where
# it expects the paper to be, as well as the corners of the paper, to calibrate before drawing
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import time

from draw_lines import (
PAPER_HEIGHT ,
LEFT_PAPER_CORNER_ABS,
PAPER_WIDTH,
PAPER_HEIGHT,
PEN_DISPLACEMENT,
)

SLEEP_TIME = 4
PLACE_PAPER_HOVER = 0.15


bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
    robot_model='rx200',
    group_name='arm',
    gripper_name='gripper',
)

# init the robot
robot_startup()
bot.arm.set_trajectory_time(1.5)

# go to the default home pose
bot.arm.go_to_home_pose()
time.sleep(3)

# go to the bottom left corner of the paper
print(f"Going to bottom left corner of the paper: {LEFT_PAPER_CORNER_ABS[0] , LEFT_PAPER_CORNER_ABS[1], PLACE_PAPER_HOVER}")
bot.arm.set_ee_pose_components(LEFT_PAPER_CORNER_ABS[0], LEFT_PAPER_CORNER_ABS[1], PLACE_PAPER_HOVER)
time.sleep(SLEEP_TIME)

# top left corner
print(f"Going to top left corner of the paper: {LEFT_PAPER_CORNER_ABS[0] + PAPER_HEIGHT , LEFT_PAPER_CORNER_ABS[1], PLACE_PAPER_HOVER}")
bot.arm.set_ee_pose_components(LEFT_PAPER_CORNER_ABS[0] + PAPER_HEIGHT , LEFT_PAPER_CORNER_ABS[1], PLACE_PAPER_HOVER)
time.sleep(SLEEP_TIME)

# top right corner
print(f"Going to top right corner of the paper: {LEFT_PAPER_CORNER_ABS[0] - PAPER_HEIGHT , LEFT_PAPER_CORNER_ABS[1] + PAPER_WIDTH, PLACE_PAPER_HOVER}")
bot.arm.set_ee_pose_components(LEFT_PAPER_CORNER_ABS[0] + PAPER_HEIGHT , LEFT_PAPER_CORNER_ABS[1] - PAPER_WIDTH, PLACE_PAPER_HOVER)
time.sleep(SLEEP_TIME)

# top left corner
print(f"Going to bottom right corner of the paper: {LEFT_PAPER_CORNER_ABS[0] , LEFT_PAPER_CORNER_ABS[1] - PAPER_WIDTH, PLACE_PAPER_HOVER}")
bot.arm.set_ee_pose_components(LEFT_PAPER_CORNER_ABS[0] , LEFT_PAPER_CORNER_ABS[1] - PAPER_WIDTH, PLACE_PAPER_HOVER)
time.sleep(SLEEP_TIME)

# go to paper midpoint and hover
print(f"Hovering over paper midpoint like with pen at: {LEFT_PAPER_CORNER_ABS[0] + PAPER_HEIGHT/2, LEFT_PAPER_CORNER_ABS[1] - PAPER_WIDTH/2, LEFT_PAPER_CORNER_ABS[2] + PEN_DISPLACEMENT}")
bot.arm.set_ee_pose_components(LEFT_PAPER_CORNER_ABS[0] + PAPER_HEIGHT/2, LEFT_PAPER_CORNER_ABS[1] - PAPER_WIDTH/2, LEFT_PAPER_CORNER_ABS[2] + PEN_DISPLACEMENT)
time.sleep(SLEEP_TIME)

print("Going to sleep and shutting down")
bot.arm.go_to_sleep_pose()
time.sleep(3)
robot_shutdown()
