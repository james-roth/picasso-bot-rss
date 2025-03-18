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

    # starts up the robot, leave 
    bot.gripper.set_pressure(0.25)
    robot_startup()


    # some sample moving code
    bot.arm.go_to_home_pose()
    print("At home position")
    time.sleep(2)

    print(bot.arm.set_ee_cartesian_trajectory(z=-0.15))
    print("moved in the z direction")

    print(bot.arm.set_ee_cartesian_trajectory(x=-0.05))
    print("moved in the x direction")
    # bot.arm.set_ee_pose_components(x=0.3)
    time.sleep(2)

    # shutdown code, leave in
    print("going to sleep")
    bot.arm.go_to_sleep_pose()
    robot_shutdown()

if __name__ == '__main__':
    main()
