import tkinter as tk

waypoints = []
start_point = None
lock_direction = None

def on_mouse_down(event):
    global start_point, lock_direction
    start_point = (event.x, event.y)
    lock_direction = None  # Reset direction lock

def on_mouse_drag(event):
    global lock_direction
    if start_point is None:
        return

    x0, y0 = start_point
    dx, dy = abs(event.x - x0), abs(event.y - y0)

    if lock_direction is None:
        # Determine dominant direction to lock
        lock_direction = 'x' if dx > dy else 'y'

    if lock_direction == 'x':
        x, y = event.x, y0
    else:
        x, y = x0, event.y

    # Remove previous preview line
    canvas.delete("preview")
    # Draw new preview line
    canvas.create_line(x0, y0, x, y, fill='blue', tags="preview")

def on_mouse_up(event):
    global start_point, lock_direction
    if start_point is None or lock_direction is None:
        return

    x0, y0 = start_point
    if lock_direction == 'x':
        x, y = event.x, y0
    else:
        x, y = x0, event.y

    # Draw the final black line
    canvas.create_line(x0, y0, x, y, fill='black')
    # Store both the starting point and ending point
    waypoints.append((x0, y0, x, y))

    # Reset
    start_point = None
    lock_direction = None
    canvas.delete("preview")

def save_path():
    with open("waypoints.txt", "w") as f:
        for x0, y0, x1, y1 in waypoints:
            # Store four comma-separated values: start_x, start_y, end_x, end_y
            f.write(f"{x0},{y0},{x1},{y1}\n")
    print("Saved path to waypoints.txt")

# GUI setup
root = tk.Tk()
canvas = tk.Canvas(root, width=1100, height=850, bg='white')
canvas.pack()

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
root.bind("<Return>", lambda e: save_path())  # Press Enter to save

root.mainloop()
