import numpy as np

# # The BOTTOM left corner of the paper is (0, 0)
# # The TOP right corner of the paper is (CANVAS_WIDTH, CANVAS_HEIGHT)
# x_min_draw = 0
# x_max_draw = CANVAS_WIDTH
# y_min_draw = 0
# y_max_draw = CANVAS_HEIGHT
# # Paper values:
# PAPER_WIDTH = 0.29
# PAPER_HEIGHT = 0.19
# # The BOTTOM left corner of the paper w.r.t the robot's base frame.
# LEFT_PAPER_CORNER_ABS = np.array([0.25, 0.14, 0.05])

from constants import (
    PAPER_WIDTH,
    PAPER_HEIGHT,
    x_min_draw,
    x_max_draw,
    y_min_draw,
    y_max_draw,
    LEFT_PAPER_CORNER_ABS
)


def scale_paper_points(lines):
    """
    A the workhorse method for load_waypoints, so this functionality can be avilable without changing existing code.
    """
    scaled_waypoints = []
    for segment in lines:
        x0, y0, x1, y1 = segment
        assert x_min_draw <= x0 <= x_max_draw, f"Pre-scaled x0 {x0} is out of bounds"
        assert y_min_draw <= y0 <= y_max_draw, f"Pre-scaled y0 {y0} is out of bounds"
        assert x_min_draw <= x1 <= x_max_draw, f"Pre-scaled x1 {x1} is out of bounds"
        assert y_min_draw <= y1 <= y_max_draw, f"Pre-scaled y1 {y1} is out of bounds"

        # Scale the points to the robot's coordinate system
        x0_scaled = (x0 - x_min_draw) / (x_max_draw - x_min_draw) * PAPER_WIDTH
        y0_scaled = (y0 - y_min_draw) / (y_max_draw - y_min_draw) * PAPER_HEIGHT
        x1_scaled = (x1 - x_min_draw) / (x_max_draw - x_min_draw) * PAPER_WIDTH
        y1_scaled = (y1 - y_min_draw) / (y_max_draw - y_min_draw) * PAPER_HEIGHT

        assert 0 <= x0_scaled <= PAPER_WIDTH, f"Scaled x0 {x0_scaled} is out of bounds"
        assert 0 <= y0_scaled <= PAPER_HEIGHT, f"Scaled y0 {y0_scaled} is out of bounds"
        assert 0 <= x1_scaled <= PAPER_WIDTH, f"Scaled x1 {x1_scaled} is out of bounds"
        assert 0 <= y1_scaled <= PAPER_HEIGHT, f"Scaled y1 {y1_scaled} is out of bounds"

        scaled_waypoints.append((x0_scaled, y0_scaled, x1_scaled, y1_scaled))

    return scaled_waypoints

def load_waypoints(filename="waypoints.txt"):
    """
    Loads waypoints from waypoints.txt and scales them to the robot's coordinate system.
    DOES NOT apply any translation or rotation to the points (to put them in a drawable coordinate system for the arm).

    Assumes the waypoints are in a coordinate system where the origin is at the bottom left corner of the canvas],
    and both the x and y axes are positive in the right and up directions, respectively.

    robot_paper_width_x: The width of the paper in the robot's coordinate system.
    robot_paper_height_y: The height of the paper in the robot's coordinate system.
    filename: The name of the file containing the waypoints.
    """

    assert PAPER_WIDTH > 0, f"Width of paper in robot's coordinate system must be positive"
    assert PAPER_HEIGHT > 0, f"Height of paper in robot's coordinate system must be positive"

    # verify inputs are valid
    waypoints = []

    with open(filename, "r") as f:
        for line in f:
            values = line.strip().split(",")
            if len(values) == 4:
                x0, y0, x1, y1 = map(int, values)
                waypoints.append((x0, y0, x1, y1))

    scaled_waypoints = scale_paper_points(waypoints)
    return scaled_waypoints

def convert_to_robot_coords(lines: list[list[float]]) -> list[list[float]]:
    """
    Converts coordinates for lines from the paper's coordinate frame to the robot's coordinate frame.
    The paper's coordinate frame is defined as the bottom left corner of the paper being (0, 0) and the top right corner being (WIDTH, HEIGHT).
    to the one used by the robot's drawing functions so that coordinates on the paper are drawn
    in the correct orientation by the robot.

    In the ROBOT's coordinate frame:

            + X
            
      + Y   Paper  - Y
            here     
    
            ROBOT
    
            - X

    In the frame of the paper:
    0, HEIGHT               WIDTH, HEIGHT



    0, 0                    WIDTH, 0
    """ 
    new_lines = []
    for paper_point in lines:
        # for lines represented as 2 points like (x0, y0, x1, y1)
        if len(paper_point) == 4:
            # swap the points as the x axis of the robot is the y axis of the paper, and vice versa
            # ie. (x, y) in paper coords = (y, x) in robot coords
            y0, x0, y1, x1 = paper_point

            # Convert to robot's coordinate frame, POINTS ARE ALREADY SCALED TO ROBOT'S FRAME
            x0 = LEFT_PAPER_CORNER_ABS[0] + x0
            y0 = LEFT_PAPER_CORNER_ABS[1] - y0
            x1 = LEFT_PAPER_CORNER_ABS[0] + x1
            y1 = LEFT_PAPER_CORNER_ABS[1] - y1

            new_lines.append([x0, y0, x1, y1])
        # for 2D points, we need to convert them to 3D points by adding the z coordinate
        elif len(paper_point) == 2:
            # swap the points as the x axis of the robot is the y axis of the paper, and vice versa
            # ie. (x, y) in paper coords = (y, x) in robot coords
            y0, x0 = paper_point

            # Convert to robot's coordinate frame, POINTS ARE ALREADY SCALED TO ROBOT'S FRAME
            x0 = LEFT_PAPER_CORNER_ABS[0] + x0
            y0 = LEFT_PAPER_CORNER_ABS[1] - y0

            new_lines.append([x0, y0])

    return new_lines

# ## Some basic test code
# if __name__ == "__main__":
#     # Example usage
#     x_min_robot = -0.2
#     x_max_robot = 0.2
#     y_min_robot = -0.2
#     y_max_robot = 0.2

#     waypoints = load_waypoints(
#         robot_paper_width_x=x_max_robot - x_min_robot,
#         robot_paper_height_y=y_max_robot - y_min_robot,
#         filename="waypoints.txt"
#     )
#     print(waypoints)

#     # Convert to robot coordinates
#     robot_coords = convert_to_robot_coords(waypoints)
#     for segment in robot_coords:
#         print(f"Segment: {segment}")