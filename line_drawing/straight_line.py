import tkinter as tk

waypoints = []
start_point = None
CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 850

def set_bottom_left_origin(x0, y0, x1, y1):
    """
    The drawing software sets the origin to the top left of the window. This function converts
    the points to an origin in the bottom left, in order to standardize our coordinate systems.

    Does some bounding as the software can get points at negative values and this is the best way to solve it.
    """
    # print(f"Starting points: ({x0}, {y0}), ({x1}, {y1})")

    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = max(0, x1)
    y1 = max(0, y1)
    x0 = min(CANVAS_WIDTH, x0)
    y0 = min(CANVAS_HEIGHT, y0)
    x1 = min(CANVAS_WIDTH, x1)
    y1 = min(CANVAS_HEIGHT, y1)

    # Convert to bottom-left origin
    y0 = CANVAS_HEIGHT - y0
    y1 = CANVAS_HEIGHT - y1

    # print(f"Converted points: ({x0}, {y0}), ({x1}, {y1})")

    # Return the points in the new coordinate system
    assert 0 <= x0 <= CANVAS_WIDTH, f"Start x coord {x0} is out of bounds"
    assert 0 <= y0 <= CANVAS_HEIGHT, f"Start y coord {y0} is out of bounds"
    assert 0 <= x1 <= CANVAS_WIDTH, f"End x coord {x1} is out of bounds"
    assert 0 <= y1 <= CANVAS_HEIGHT, f"End y coord {y1} is out of bounds"

    return x0, y0, x1, y1

def on_mouse_down(event):
    global start_point, lock_direction
    start_point = (event.x, event.y)

def on_mouse_drag(event):
    if start_point is None:
        return

    x0, y0 = start_point
    # Remove previous preview line
    canvas.delete("preview")
    # Draw new preview line
    canvas.create_line(x0, y0, event.x, event.y, fill='blue', tags="preview")

def on_mouse_up(event):
    global start_point
    if start_point is None:
        return

    x0, y0 = start_point

    # Draw the final black line
    canvas.create_line(x0, y0, event.x, event.y, fill='black')
    
    points = set_bottom_left_origin(x0, y0, event.x, event.y)
    # Store both the starting point and ending point
    waypoints.append(points)

    # Reset
    start_point = None
    canvas.delete("preview")

def save_path(root):
    with open("waypoints.txt", "w") as f:
        for x0, y0, x1, y1 in waypoints:
            # Store four comma-separated values: start_x, start_y, end_x, end_y
            f.write(f"{x0},{y0},{x1},{y1}\n")
    print("Saved path to waypoints.txt")
    root.destroy()

# GUI setup
root = tk.Tk()


label = tk.Label(root, text="Press Enter To Save Your Drawing And Close This Window")
label.pack(pady=20, padx=20)

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
canvas.pack()

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
root.bind("<Return>", lambda e: save_path(root))  # Press Enter to save

root.mainloop()
