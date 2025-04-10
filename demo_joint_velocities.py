# Robot-specific imports
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS

# Others
import numpy as np
import time

from line_drawing.constants import (
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

def get_eff_coords(robot: InterbotixManipulatorXS) -> np.ndarray:
    """
    Gets the x, y, z coordinates of the robot's end effector as a numpy array.
    """
    ee_pose = robot.arm.get_ee_pose()
    cur_xyz = np.array(ee_pose)[:-1, -1].T
    return cur_xyz

def get_joint_names_and_efforts(bot: InterbotixManipulatorXS):
    info = bot.arm.group_info
    names = info.joint_names
    efforts = bot.arm.get_joint_efforts()
    assert len(efforts) == len(names)

    name_to_effort_map = {}
    for i in range(0, len(names)):
        name = names[i]
        name_to_effort_map[name] = efforts[i]
    return name_to_effort_map

def has_stopped_by_position(bot: InterbotixManipulatorXS, epsilon=0.001, interval=0.1):
    state1 = get_eff_coords(bot)
    time.sleep(interval)
    state2 = get_eff_coords(bot)
    for p1, p2 in zip(state1, state2):
        if abs(p2 - p1) > epsilon:
            return False
    return True

def main():
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
    bot.gripper.release()
    time.sleep(1)
    bot.gripper.grasp()
    time.sleep(SLEEP_TIME)

    efforts = bot.arm.get_joint_efforts()
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=-0.25, moving_time=3)

    mA_threshold = 650
    vel_over_0 = False
    times_back_0 = 0


    while True:
        # names_efforts = get_joint_names_and_efforts(bot)
        # print(names_efforts)
        # print("_______________________________________\n")
        # for joint in names_efforts:
        #     if names_efforts[joint] >= mA_threshold:
        #         raise ValueError(f"Joint over threshold: {joint}, value: {names_efforts[joint]}")
            # print(bot.core. .robot_get_operating_mode(joint))
        
        # print(bot.core.robot_get_joint_states())
        states = bot.core.robot_get_joint_states()

        all_0s = True
        for vel in states.velocity:
            if vel > 0.0:
                print(f"VEL over 0.0: {vel}")
                all_0s = False
                if not vel_over_0:
                    vel_over_0 = True
        for eff in states.effort:
            if eff > mA_threshold:
                print(f"EFFORT over 0.0: {eff}")
        
        if has_stopped_by_position(bot, interval=0.125):
            print("Capturing joint positions")
            bot.arm.capture_joint_positions()
            print("Made contact with paper, stopping ALL motion")
            time.sleep(2)
            bot.arm.go_to_home_pose()
            time.sleep(2)
            bot.gripper.release()
            bot.arm.go_to_sleep_pose()
            time.sleep(3)
            robot_shutdown()
            break


        # # motors were moving and have now stopped
        # if vel_over_0 and all_0s:
        #     times_back_0 += 1
        #     print(f"stopped moving: {times_back_0}")

        #     if times_back_0 >= 5:
        #         print(states)

        #         print("Made contact with paper, stopping ALL motion")
        #         bot.
        #         time.sleep(2)
        #         bot.arm.go_to_home_pose()
        #         time.sleep(2)
        #         bot.gripper.release()
        #         bot.arm.go_to_sleep_pose()
        #         time.sleep(3)
        #         robot_shutdown()
        #         break
        # else: 
        #     times_back_0 = 0
        #     print("reset")


        time.sleep(0.05)

        

if __name__ == "__main__":
    main()