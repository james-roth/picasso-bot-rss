
x_min_robot = .2
x_max_robot = .35
x_min_draw = 0
x_max_draw = 850

y_min_robot = -.1
y_max_robot = .1
y_min_draw = 0
y_max_draw = 1100

x_range = x_max_robot - x_min_robot
y_range = y_max_robot - y_min_robot

def load_waypoints(filename="waypoints.txt"):
    waypoints = []
    with open(filename, "r") as f:
        for line in f:
            values = line.strip().split(",")
            if len(values) == 4:
                x0, y0, x1, y1 = map(int, values)
                waypoints.append((x0, y0, x1, y1))

    scaled_waypoints = []
    for segment in waypoints:
        y0, x0, y1, x1 = segment
        x_start_scaled = ((x0 * x_range) / x_max_draw) + x_min_robot
        y_start_scaled = ((y0 * y_range) / y_max_draw) + y_min_robot
        x_end_scaled = ((x1 * x_range) / x_max_draw) + x_min_robot
        y_end_scaled = ((y1 * y_range) / y_max_draw) + y_min_robot
        scaled_waypoints.append((x_start_scaled, y_start_scaled, x_end_scaled, y_end_scaled))
    return scaled_waypoints
