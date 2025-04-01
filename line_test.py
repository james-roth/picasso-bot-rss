import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np

#new import, have to pip install iirc
import modern_robotics as mr

def get_bot_coords(robot):
    ee_pose = robot.arm.get_ee_pose()
    cur_xyz = np.array(ee_pose)[:-1, -1].T
    # print(f'Current robot pose: {cur_xyz}')
    # roll_pitch_yaw = 
    return cur_xyz

def main():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
            robot_model='rx200',
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
    # bot.arm.set_ee_cartesian_trajectory(z=-0.14, x=-0.05, moving_time=1, wp_period=0.05) #pitch=-0.15,
    # bot.arm.set_ee_cartesian_trajectory(pitch=-0.5, moving_time=1, wp_period=0.05)

    # time.sleep(SLEEP_TIME)
    time.sleep(SLEEP_TIME)
    print("Moved robot end effector downwards")

    # get the robot's current x, y, z for the end effector, to calculate a move
    cur_xyz = get_bot_coords(bot)
    time.sleep(SLEEP_TIME)
    always_z = cur_xyz[2]

    # generate points to move the robot from (pt A to B) as absolute positions
    translation_xyz = np.array([-0.15, 0, 0])

    print("Starting line movement calculations")
    # calculate waypoints to move the robot between
    num_waypoints = 20
    WAYPOINT_SLEEP_TIME = 0.25/num_waypoints
    TOTAL_MOVING_TIME = 1.5
    # print(bot.arm.set_ee_cartesian_trajectory(translation_xyz[0], translation_xyz[1], translation_xyz[2], moving_time=1, wp_period=0.025))

    # print(f"Starting move with {num_waypoints} waypoints, sleep time between waypoints: {WAYPOINT_SLEEP_TIME}")
    # Actually move the bot, 0y0->x1y1

    new_xyz = get_bot_coords(bot) + translation_xyz

    T = np.eye(4)  # Start with an identity matrix (4x4)
    # T[:3, :3] # keep rotation as identitiy
    T[:3, 3] = new_xyz

    print(f"Starting position: {get_bot_coords(bot)}")

    # print(T)
    # bot.arm.set_ee_pose_matrix(T, moving_time=1.5)
    print(bot.arm.set_ee_cartesian_trajectory(translation_xyz[0], translation_xyz[1], translation_xyz[2], moving_time=0.5))

    # expected_z = get_bot_coords(bot)[2]
    # for i in range(num_waypoints):
    #     x = translation_xyz[0]/num_waypoints
    #     y = translation_xyz[1]/num_waypoints
    #     eff_xyz = get_bot_coords(bot)
    #     z = expected_z - eff_xyz[2]

    #     bot.arm.set_ee_arc_tragectory

    #     print(f"Attempting move with x: {x}, y: {y} z: {z} translation")
    #     print(f"Current position: {eff_xyz}")
    #     success = bot.arm.set_ee_cartesian_trajectory(x, y, z, moving_time=0.1, wp_accel_time=0.05) #, moving_time=TOTAL_MOVING_TIME/num_waypoints, wp_period=TOTAL_MOVING_TIME/num_waypoints/5)
    #     print(f"Waypoint moving status: {success}")
    #     time.sleep(WAYPOINT_SLEEP_TIME)
    
    print(f"Final position: {get_bot_coords(bot)}")
    time.sleep(SLEEP_TIME)
    print(f"Final position after sleep: {get_bot_coords(bot)}")

    print("Done with attempted moves, shutting down")

    bot.arm.set_trajectory_time(1.25)
    print("Going to home pose")
    bot.arm.go_to_home_pose()
    time.sleep(SLEEP_TIME)
    print("Going to sleep pose")
    bot.arm.go_to_sleep_pose()
    time.sleep(SLEEP_TIME)

    #release the pen, if holding any
    bot.gripper.release()

    robot_shutdown()


def main2():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
        robot_model='rx200',
        group_name='arm',
        gripper_name='gripper',
    )
    
    SLEEP_TIME = 3.0
    # print(bot.arm.group_info)
    robot_startup()
    bot.arm.set_trajectory_time(1.5)
    bot.gripper.set_pressure(0.7)
    

    bot.arm.go_to_home_pose()
    bot.arm.set_ee_cartesian_trajectory(z=-0.2, y=-0.1)
    # bot.arm.set_ee_pose_components(x=0.3, blocking=True)
    time.sleep(SLEEP_TIME)
    print("Went to home pose")
    bot.gripper.release()
    time.sleep(2)
    bot.gripper.grasp()

    print(f"Starting position: {get_bot_coords(bot)}")

    # this function is "the best", but it still has a million problems, inlcuding but not limited to:
    # - it still can only keep a semi-consistent z-level and thus is a pretty shitty drawer
    # - our arm does not have enough DOF to let it move in the y direction with this function, thanks interbotix very cool
    bot.arm.set_ee_cartesian_trajectory(-0.20, 0, 0, moving_time=1, wp_accel_time=0.25)
    time.sleep(6)
    print(f"Ending position: {get_bot_coords(bot)}")

    # new_xyz = get_bot_coords(bot) + np.array([0.1, 0, 0])
    # T = np.eye(4)
    # T[:3, 3] = new_xyz
    # print(f"Starting position: {get_bot_coords(bot)}")
    # print(T)
    # bot.arm.set_ee_pose_matrix(T, moving_time=3.5, accel_time=0.5, custom_guess=bot.arm.joint_commands)
    # time.sleep(5)
    # print(f"Ending position: {get_bot_coords(bot)}")

    bot.arm.set_trajectory_time(2)
    bot.arm.go_to_sleep_pose(blocking=True)
    bot.gripper.release()
    time.sleep(SLEEP_TIME)
    robot_shutdown()

if __name__ == "__main__": 
    main2()
