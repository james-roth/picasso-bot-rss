import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np

#new import, have to pip install iirc
import modern_robotics as mr

def main():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
            robot_model='px150',
            group_name='arm',
            gripper_name='gripper',
        )
    
    SLEEP_TIME = 3.0
    # print(bot.arm.group_info)
    robot_startup()
    bot.arm.go_to_home_pose()
    time.sleep(SLEEP_TIME)
    print("Went to home pose")

    # move the robot down to make contact with the paper
    bot.arm.set_ee_cartesian_trajectory(z=-0.15)
    time.sleep(SLEEP_TIME)
    print("Moved robot end effector downwards")

    # get the robot's current x, y, z for the end effector, to calculate a move
    cur_xyz = np.array(bot.arm.get_ee_pose())[:-1, -1].T
    print(f'Current robot pose: {cur_xyz}')
    time.sleep(SLEEP_TIME)

    # generate points to move the robot from (pt A to B) as absolute positions
    transformation_xyz = np.array([0.15, 0, 0])
    point_a = cur_xyz
    point_b = cur_xyz + transformation_xyz

    print("Starting line movement calculations")
    # calculate waypoints to move the robot between
    num_waypoints = 10
    x_points = np.linspace(point_a[0], point_b[0], num=num_waypoints)
    y_points = np.linspace(point_a[1], point_b[1], num=num_waypoints)


    WAYPOINT_SLEEP_TIME = 0.4
    # set a faster moving time
    bot.arm.set_trajectory_time(0.4)

    print(f"Starting move with {num_waypoints} waypoints, sleep time between waypoints: {WAYPOINT_SLEEP_TIME}")
    # Actually move the bot, 0y0->x1y1
    for x, y in zip(x_points, y_points):
        success = bot.arm.set_ee_pose_components(x=x, z=.1, y=y, blocking=False)
        print(f"Waypoint moving status: {success[1]}")
        time.sleep(WAYPOINT_SLEEP_TIME)
    
    time.sleep(SLEEP_TIME)
    print("Done with attempted moves, shutting down")

    bot.arm.set_trajectory_time(2)
    print("Going to home pose")
    bot.arm.go_to_home_pose()
    time.sleep(SLEEP_TIME)
    print("Going to sleep pose")
    bot.arm.go_to_sleep_pose()
    time.sleep(1)

    #release the pen, if holding any
    bot.gripper.release()

    robot_shutdown()


if __name__ == "__main__": 
    main()
