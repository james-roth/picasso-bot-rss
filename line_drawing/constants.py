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
PEN_DISPLACEMENT = 0.015
# ensure the pen is always a certain distance above the paper
PAPER_HOVER = round(0.135 + PEN_DISPLACEMENT, 4)
# The BOTTOM left corner of the paper w.r.t the robot's base frame.
LEFT_PAPER_CORNER_ABS = np.array([0.25, 0.14, 0.05])
PAPER_WIDTH = 0.30
PAPER_HEIGHT = 0.18

### ROBOT VALUES:
# Robot arm values:
GRIPPER_PRESSURE = 1.0
TRAJECTORY_TIME = 1.2
ACCEL_TIME = TRAJECTORY_TIME/5
SLEEP_TIME = 3.0
# for calibration only
CALIBRATION_SLEEP_TIME = 4.0
