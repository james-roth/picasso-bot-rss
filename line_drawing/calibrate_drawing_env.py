# The purpose of this file is to have the robot move its end effector to where
# it expects the paper to be, as well as the corners of the paper, to calibrate before drawing
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import time
from scale_points import convert_to_robot_coords, scale_paper_points, increase_motor_accuracies
from constants import (
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    PAPER_HOVER,
    PEN_DISPLACEMENT,
    LEFT_PAPER_CORNER_ABS,
    CALIBRATION_SLEEP_TIME,
    SLEEP_TIME,
    REG_DELTA,
    JOINT_DEFAULTS
)

bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
    robot_model='rx200',
    group_name='arm',
    gripper_name='gripper',
)

# init the robot
robot_startup()

increase_motor_accuracies(bot)

bot.arm.set_trajectory_time(1.5)

# go to the default home pose
bot.arm.go_to_home_pose()
time.sleep(CALIBRATION_SLEEP_TIME)

# PAPER_HOVER = LEFT_PAPER_CORNER_ABS[2] + PEN_DISPLACEMENT

paper_coords = [
    [0, 0, PAPER_HOVER],
    [0, CANVAS_HEIGHT, PAPER_HOVER],
    [CANVAS_WIDTH, CANVAS_HEIGHT, PAPER_HOVER],
    [CANVAS_WIDTH, 0, PAPER_HOVER],
    [CANVAS_WIDTH/2, CANVAS_HEIGHT/2, LEFT_PAPER_CORNER_ABS[2] + PEN_DISPLACEMENT],
]
msg_strings = [
    "bottom left corner",
    "top left corner", 
    "top right corner",
    "bottom right corner",
    "hover over the middle",
]

for i in range(0,5):
    coords = paper_coords[i]
    x_y = scale_paper_points([[coords[0], coords[1], 1, 1]])[0][0:2] # we only care about the first 2 points, this is easier than changing scale_paper_points
    x_y = convert_to_robot_coords([x_y])
    x_y[0].append(coords[2])
    x_y_z = x_y[0]
    print(x_y_z)
    print(f"Going to {msg_strings[i]} of the paper: {x_y_z[0], x_y_z[1], x_y_z[2]}")
    bot.arm.set_ee_pose_components(x_y_z[0], x_y_z[1], x_y_z[2])
    time.sleep(CALIBRATION_SLEEP_TIME)

print("Going to sleep and shutting down")
bot.arm.go_to_sleep_pose()
time.sleep(3)
robot_shutdown()
