import numpy as np

### DRAWING CANVAS values:
# The BOTTOM left corner of the paper is (0, 0)
# The TOP right corner of the paper is (CANVAS_WIDTH, CANVAS_HEIGHT)
CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 850
x_min_draw = 0
x_max_draw = CANVAS_WIDTH
y_min_draw = 0
y_max_draw = CANVAS_HEIGHT

### PHYSICAL PAPER VALUES:
# PEN_DISPLACEMENT = 0.015
PEN_DISPLACEMENT = 0.05
# ensure the pen is always a certain distance above the paper
PAPER_HOVER = round(0.135 + PEN_DISPLACEMENT, 4)
# The BOTTOM left corner of the paper w.r.t the robot's base frame.
LEFT_PAPER_CORNER_ABS = np.array([0.25, 0.12, 0.05])
# Y Coord of the robot frame
PAPER_WIDTH = 0.24
# X Coord of the robot frame
PAPER_HEIGHT = 0.18
# the eucliden distance that the pen should not be picked up if the next point is close enoughhhhhh to
PEN_MOVEMENT_THRESHOLD = 0.05

### ROBOT VALUES:
# Robot arm values:
GRIPPER_PRESSURE = 1.0
TRAJECTORY_TIME = 1
ACCEL_TIME = TRAJECTORY_TIME/4
SLEEP_TIME = 2.5
# for calibration only
CALIBRATION_SLEEP_TIME = 4.0

# how much to up the position_p_gain register to increase the motor's accuracy
REG_DELTA = 350
# the default values of the position_p_gain registers, mapped to each joint's name
JOINT_DEFAULTS = {'waist': 640, 'shoulder': 800, 'elbow': 800, 'wrist_angle': 640, 'wrist_rotate': 640}