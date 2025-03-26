import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np

#new import, have to pip install iirc
import modern_robotics as mr

#M and Slist arrays from Interbotix
M = np.array([[1.0, 0.0, 0.0, 0.358575],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.25457],
    [0.0, 0.0, 0.0, 1.0]])
Slist = np.array([[0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, -0.10457, 0.0, 0.0],
        [0.0, 1.0, 0.0, -0.25457, 0.0, 0.05],
        [0.0, 1.0, 0.0, -0.25457, 0.0, 0.2],
        [1.0, 0.0, 0.0, 0.0, 0.25457, 0.0]]).T

def inverse_kinematics(target_pos, roll=0, pitch=0):
    """
    computes the joint angles required to reach target_pos while maintaining roll and pitch.
    Uses Newton-Raphson iterative method for inverse kinematics (from the modern_robotics library)
    """
    R = mr.RollPitchYawToSO3(roll, pitch, 0)  # Keep yaw as 0
    T_target = np.eye(4)
    T_target[:3, :3] = R
    T_target[:3, 3] = target_pos
    
    q0 = np.zeros(5)  # Initial guess for joint angles
    joint_angles, success = mr.IKinSpace(Slist, M, T_target, q0, 1e-4, 1e-4)
    
    if not success:
        raise ValueError("IK solution did not converge")
    
    return joint_angles

def move_to_target(bot, start_pos, target_pos, roll=0, pitch=0, duration=2.0):
    """
    Moves the arm in a straight-line trajectory from start_pos tuah target_pos,
    maintaining roll and pitch angles (or not, im not your mom)
    """
    #50hz control loop (50 waypoints per second), can be decreased or increased, if so, make sure to change the moving_time or accel_time
    num_steps = int(duration * 50)
    waypoints = np.linspace(start_pos, target_pos, num_steps)
    
    for point in waypoints:
        joint_angles = inverse_kinematics(point, roll, pitch)
        #no blocking since smooth iterative/continuous moving
        bot.arm.set_joint_positions(joint_angles, blocking=False)
        #20ms step time between waypoints (could be removed, used for initial testing)
        bot.arm.sleep(0.02)

def main():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
            robot_model='px150',
            group_name='arm',
            gripper_name='gripper',
        )

    print(bot.arm.group_info)
    robot_startup()

    #give some time to place the pen in
    bot.gripper.release()
    time.sleep(4.0)

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
    #print("Draw Line")
    #bot.arm.set_ee_cartesian_trajectory(x=0.05, moving_time=2.0)

    #========Thing that we have to test=========
    #1. get the current pose of the arm
    #2. calculate/hypothesize a point where we want it to go
    #3. call `move_to_target` from start to end, possibly updating the roll/pitch values or waypoint amnt

    print("Done operation")
    bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()

    #release the pen
    bot.gripper.release()

    robot_shutdown()

if __name__ == '__main__':
    main()
