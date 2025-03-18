import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np


def main():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
            robot_model='px150',
            group_name='arm',
            gripper_name='gripper',
        )

    print(bot.arm.group_info)
    robot_startup()
    bot.gripper.set_pressure(2.0)
    bot.gripper.release()
    bot.gripper.grasp()
    bot.arm.go_to_home_pose()
    print("Trying to adjust the cartesian end effector")
    print(bot.arm.set_ee_cartesian_trajectory(z=-0.15))
    print("moved in the z direction")
    print(bot.arm.set_ee_cartesian_trajectory(x=-0.05))
    print("Testing Marker/Pencil")
    bot.arm.set_single_joint_position(joint_name='waist', position=np.pi/12)
    bot.arm.set_single_joint_position(joint_name='waist', position=-np.pi/12)
    print("Done Testing")
    print("Draw Line")
    bot.arm.set_ee_cartesian_trajectory(x=0.05)
    print("Done operation")
    bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()

    robot_shutdown()

if __name__ == '__main__':
    main()
