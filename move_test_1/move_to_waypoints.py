import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np
from scale_points import load_waypoints

def main():
    bot: InterbotixManipulatorXS = InterbotixManipulatorXS(
            robot_model='rx200',
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
            #doing this to the trajectory as we only want a singular waypoint (strict path planning)
            move_time=1.0 #seconds
            success = bot.arm.set_ee_cartesian_trajectory(moving_time=move_time,
                wp_moving_time=move_time,
                wp_accel_time=(move_time/2),
                wp_period=move_time,
                **kwargs)

        if success:
            method = "absolute pose" if absolute else "relative trajectory"
            desc = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            # print(f"Moved using {method}: {desc}")
        else:
            print(f"Failed to move with args: {kwargs}")

        time.sleep(sleep_time)
        print("Sleep done")
    
    
    def compute_adjustments(x, y):
        """
        Compute the y and z adjustments based on the position in the xy-plane.

        Args:
        x (float): The x coordinate.
        y (float): The y coordinate.

        Returns:
            tuple: Adjusted (y, z)
        """
        # Scaling factors
        k_z = 0.03  # Influence of y on z
        k_x = 0.02  # Influence of x on y

        # Reference min/max values
        y_min, y_max = -0.1, 0.1
        x_min, x_max = 0.2, 0.35

        # Compute normalized factors (range -1 to 1)
        y_factor = (y - y_min) / (y_max - y_min) * 2 - 1                
        # Maps y in [-0.1, 0.1] to [-1, 1]
        x_factor = (x - x_min) / (x_max - x_min)  
        # Maps x in [0.2, 0.35] to [0, 1]

        # Compute z adjustment based on y movement
        z_adjustment = k_z * (1 - x_factor)

        # Compute y adjustment based on x movement (higher at min/max x)
        x_adjustment = -k_x * (1 - abs(y_factor))  # Maximum boost near x_min/x_max

        return x_adjustment, z_adjustment
    
    # starts up the robot, leave 
    bot.gripper.set_pressure(1.0)
    robot_startup()

    # some sample moving code
    bot.arm.go_to_home_pose()
    time.sleep(2)
    print("At home position")

    bot.gripper.release()
    print('put marker in the gripper')
    time.sleep(3)
    bot.gripper.grasp()
    time.sleep(2)

    waypoints = load_waypoints()
    print(waypoints)

    for segment in waypoints:
        x0, y0, x1, y1 = segment
        # Move to initial point on the line
        move(x=x1, z=.1, y=y1, blocking=False, absolute=True)
        print(f"Moved to initial point:{x1, y1}")

        num_waypoints = 5 #(min 2)amnt of waypoints we manually generate
        x_points = np.linspace(x0, x1, num=num_waypoints)
        y_points = np.linspace(y0, y1, num=num_waypoints)
        
        z_const = 0.1  # Still skipping some points (need to figure out this z constant val)

        # Interate through intermediate waypoints
        for x, y in zip(x_points[9::-1], y_points[9::-1]):
            x_adjust, z_adjust = compute_adjustments(x, y)
            print(f"Waypoint: {x+x_adjust,.1+z_adjust,y}")

            if (abs(x1 - x0) < 0.003):
                print("Horizontal Line")
                move(x=x + x_adjust, z=z_const, y=y, blocking=False, absolute=True)
            else:
                print("Vertical Line")
                move(x=x, z=z_const + z_adjust, y=y, blocking=False, absolute=True)
                
        print(f"Moved to end point: {x0, y0}")
    bot.arm.go_to_home_pose()
    time.sleep(2)
    print("going to sleep")
    bot.gripper.release()
    bot.arm.go_to_sleep_pose()
    time.sleep(2) #just so we avoid the "cannot destroy destroyable" error
    robot_shutdown()

if __name__ == '__main__':
    main()
