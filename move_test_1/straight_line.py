import tkinter as tk

waypoints = []
start_point = None

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
    # Store both the starting point and ending point
    waypoints.append((x0, y0, event.x, event.y))

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

canvas = tk.Canvas(root, width=1100, height=850, bg='white')
canvas.pack()

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
root.bind("<Return>", lambda e: save_path(root))  # Press Enter to save

root.mainloop()
