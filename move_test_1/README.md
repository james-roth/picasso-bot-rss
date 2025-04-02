## How to start using this code

# Must be running Linux Ubuntu 22.04 with ROS2 installed and following this guide:
[Getting Started](https://docs.trossenrobotics.com/interbotix_xsarms_docs/getting_started.html)

# Step 1

Run this command which will prompt lines to be drawn
`python3 draw_line.py`

# Step 2
In a seperate terminal run this command
`ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=rx200`

# Step 3
Run this command which will operate the robot
`python3 move_to_waypoints.py`
