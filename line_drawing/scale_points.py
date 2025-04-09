from straight_line import CANVAS_WIDTH, CANVAS_HEIGHT
import numpy as np

# The BOTTOM left corner of the paper is (0, 0)
# The TOP right corner of the paper is (CANVAS_WIDTH, CANVAS_HEIGHT)
x_min_draw = 0
x_max_draw = CANVAS_WIDTH
y_min_draw = 0
y_max_draw = CANVAS_HEIGHT
# Paper values:
PAPER_WIDTH = 0.29
PAPER_HEIGHT = 0.19
# The BOTTOM left corner of the paper w.r.t the robot's base frame.
LEFT_PAPER_CORNER_ABS = np.array([0.25, 0.14, 0.05])
# not a good place for these constants but the easiest way to resolve import issues for now
PEN_DISPLACEMENT = 0.015
PAPER_HOVER = 0.15


def load_waypoints(robot_paper_width_x, robot_paper_height_y, filename="waypoints.txt"):
    """
    Loads waypoints from wwaypoints.txt and scales them to the robot's coordinate system.
    DOES NOT apply any translation or rotation to the points (to put them in a drawable coordinate system for the arm).

    Assumes the waypoints are in a coordinate system where the origin is at the bottom left corner of the canvas],
    and both the x and y axes are positive in the right and up directions, respectively.

    robot_paper_width_x: The width of the paper in the robot's coordinate system.
    robot_paper_height_y: The height of the paper in the robot's coordinate system.
    filename: The name of the file containing the waypoints.
    """

    assert robot_paper_width_x > 0, f"Width of paper in robot's coordinate system must be positive"
    assert robot_paper_height_y > 0, f"Height of paper in robot's coordinate system must be positive"

    # verify inputs are valid
    waypoints = []

    with open(filename, "r") as f:
        for line in f:
            values = line.strip().split(",")
            if len(values) == 4:
                x0, y0, x1, y1 = map(int, values)
                waypoints.append((x0, y0, x1, y1))

    scaled_waypoints = []
    for segment in waypoints:
        x0, y0, x1, y1 = segment
        assert x_min_draw <= x0 <= x_max_draw, f"Pre-scaled x0 {x0} is out of bounds"
        assert y_min_draw <= y0 <= y_max_draw, f"Pre-scaled y0 {y0} is out of bounds"
        assert x_min_draw <= x1 <= x_max_draw, f"Pre-scaled x1 {x1} is out of bounds"
        assert y_min_draw <= y1 <= y_max_draw, f"Pre-scaled y1 {y1} is out of bounds"

        # Scale the points to the robot's coordinate system
        x0_scaled = (x0 - x_min_draw) / (x_max_draw - x_min_draw) * robot_paper_width_x
        y0_scaled = (y0 - y_min_draw) / (y_max_draw - y_min_draw) * robot_paper_height_y
        x1_scaled = (x1 - x_min_draw) / (x_max_draw - x_min_draw) * robot_paper_width_x
        y1_scaled = (y1 - y_min_draw) / (y_max_draw - y_min_draw) * robot_paper_height_y

        assert 0 <= x0_scaled <= robot_paper_width_x, f"Scaled x0 {x0_scaled} is out of bounds"
        assert 0 <= y0_scaled <= robot_paper_height_y, f"Scaled y0 {y0_scaled} is out of bounds"
        assert 0 <= x1_scaled <= robot_paper_width_x, f"Scaled x1 {x1_scaled} is out of bounds"
        assert 0 <= y1_scaled <= robot_paper_height_y, f"Scaled y1 {y1_scaled} is out of bounds"

        scaled_waypoints.append((x0_scaled, y0_scaled, x1_scaled, y1_scaled))
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
    assert PAPER_HEIGHT > 0, f"Height of paper in robot's coordinate system must be positive"
    assert PAPER_WIDTH > 0, f"Width of paper in robot's coordinate system must be positive"

    new_lines = []
    for point in lines:
        # for lines represented as 2 points like (x0, y0, x1, y1)
        if len(point) == 4:
            x0, y0, x1, y1 = point
            new_point = [0, 0, 0, 0]

            # Convert to robot's coordinate frame
            new_point[0] = LEFT_PAPER_CORNER_ABS[0] + ((x0 - LEFT_PAPER_CORNER_ABS[0]) * -PAPER_WIDTH)
            new_point[1] = LEFT_PAPER_CORNER_ABS[1] - ((y0 - LEFT_PAPER_CORNER_ABS[1]) * PAPER_HEIGHT)
            new_point[2] = LEFT_PAPER_CORNER_ABS[0] + ((x1 - LEFT_PAPER_CORNER_ABS[0]) * -PAPER_WIDTH)
            new_point[3] = LEFT_PAPER_CORNER_ABS[1] - ((y1 - LEFT_PAPER_CORNER_ABS[1]) * PAPER_HEIGHT)
            new_lines.append(new_point)
        # for 2D points, we need to convert them to 3D points by adding the z coordinate
        elif len(point) == 2:
            x, y = point
            new_point = [0, 0]
            # Convert to robot's coordinate frame
            new_point[0] = LEFT_PAPER_CORNER_ABS[0] + ((x - LEFT_PAPER_CORNER_ABS[0]) * -PAPER_WIDTH)
            new_point[1] = LEFT_PAPER_CORNER_ABS[1] - ((y - LEFT_PAPER_CORNER_ABS[1]) * PAPER_HEIGHT)
            new_lines.append(new_point)

    return new_lines

## Some basic test code
if __name__ == "__main__":
    # Example usage
    x_min_robot = -0.2
    x_max_robot = 0.2
    y_min_robot = -0.2
    y_max_robot = 0.2

    waypoints = load_waypoints(
        robot_paper_width_x=x_max_robot - x_min_robot,
        robot_paper_height_y=y_max_robot - y_min_robot,
        filename="waypoints.txt"
    )
    print(waypoints)

    # Convert to robot coordinates
    robot_coords = convert_to_robot_coords(waypoints)
    for segment in robot_coords:
        print(f"Segment: {segment}")