
import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np

#new import, have to pip install iirc
import modern_robotics as mr

bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
        robot_model='rx200',
        group_name='arm',
        gripper_name='gripper',
    )

robot_startup()

time.sleep(4.0)
# bot.arm.set_trajectory_time(moving_time=1)

bot.arm.go_to_home_pose()
time.sleep(4.0)
# print("Trying to adjust the cartesian end effector")

# print(bot.arm.set_ee_pose_components(x=.2, y=0.1, z=0.1))
# time.sleep(5)

# print(bot.arm.set_ee_pose_components(x=.35, y=0.1, z=0.1))
# print("Testing Marker/Pencil")

j = ['waist', 'shoulder', 'elbow', 'wrist_angle', 'wrist_rotate']
# bot.arm.set_single_joint_position(joint_name='waist', position=np.pi/2.0)
# 
# bot.arm.set_single_joint_position(joint_name=j[2], position=np.pi/2.0)
# -120 95

time.sleep(2)
bot.arm.set_single_joint_position(joint_name=j[1], position=0*(np.pi/180))
time.sleep(2)
bot.arm.set_single_joint_position(joint_name=j[2], position=-10*(np.pi/180))
time.sleep(2)
bot.arm.set_single_joint_position(joint_name=j[3], position=0*(np.pi/180))
time.sleep(2)
bot.arm.set_single_joint_position(joint_name=j[4], position=0*(np.pi/180))
time.sleep(2)


# elbow_ranges = np.linspace(-120, 95, 10)
# print(elbow_ranges)
# for range in elbow_ranges:
#     print(elbow_ranges)
#     bot.arm.set_single_joint_position(joint_name=j[2], position=range*(np.pi/180))
#     time.sleep(2)

print("Done operation")
bot.arm.go_to_home_pose()
bot.arm.go_to_sleep_pose()

# #release the pen
# bot.gripper.release()

robot_shutdown()
