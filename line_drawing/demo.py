#in this file, we give the user the choice of if they want to manually draw or choose an existing image to draw
#(either run the straight_line.py file or the image_input.py file)

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def run_script(script_name):
    #exit current and run selected script
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run {script_name}.\n{e}")
    sys.exit()

def main():
    #create a dialog box for the user to choose between "Manual Draw" and "Image Demo".
    
    root = tk.Tk()
    root.title("Select Mode")
    root.geometry("300x150")

    label = tk.Label(root, text="Choose an option:", font=("Arial", 14))
    label.pack(pady=20)

    #button for "Manual Draw"
    manual_button = tk.Button(
        root, text="Manual Draw", font=("Arial", 12), command=lambda: run_script("straight_line.py")
    )
    manual_button.pack(pady=5)

    #button for "Image Demo"
    image_button = tk.Button(
        root, text="Image Demo", font=("Arial", 12), command=lambda: run_script("image_input.py")
    )
    image_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()