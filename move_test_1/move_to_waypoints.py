import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np
from scale_points import load_waypoints

def main():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
            robot_model='px150',
            group_name='arm',
            gripper_name='gripper',
        )

    sleep_time = 5
    
    def move(absolute=False, **kwargs):
        """
        Move the end-effector using either relative Cartesian trajectory or absolute pose components.

        Args:
            absolute (bool): If True, use absolute pose via set_ee_pose_components.
                            If False (default), use relative motion via set_ee_cartesian_trajectory.
            **kwargs: x, y, z, roll, pitch, yaw (any subset, depending on function used).
        """
        if absolute:
            success = bot.arm.set_ee_pose_components(**kwargs)
        else:
            success = bot.arm.set_ee_cartesian_trajectory(**kwargs)

        if success:
            method = "absolute pose" if absolute else "relative trajectory"
            desc = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            print(f"Moved using {method}: {desc}")
        else:
            print(f"Failed to move with args: {kwargs}")

        time.sleep(sleep_time)
        print("Sleep done")
    
    # starts up the robot, leave 
    bot.gripper.set_pressure(2.0)
    robot_startup()

    # some sample moving code
    bot.arm.go_to_home_pose()
    time.sleep(2)
    print("At home position")

    bot.gripper.release()
    print('put marker in the gripper')
    time.sleep(10)
    bot.gripper.grasp()
    time.sleep(2)

    waypoints = load_waypoints()
    print(waypoints)
    for segment in waypoints:
        x0, y0, x1, y1 = segment
        move(x=x1, z=.1, y=y1, absolute=True)
        move(x=x0, z=.1, y=y0, absolute=True)

    bot.arm.go_to_home_pose()
    time.sleep(2)
    print("going to sleep")
    bot.arm.go_to_sleep_pose()
    robot_shutdown()

if __name__ == '__main__':
    main()
