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

    bot.gripper.set_pressure(0.5)
    # robot_startup()

    # bot.gripper.release()
    # bot.gripper.grasp()

    # time.sleep(10)
    # bot.gripper.release()


    # # bot.arm.go_to_home_pose()
    # bot.arm.go_to_sleep_pose()

    # robot_shutdown()

if __name__ == '__main__':
    main()