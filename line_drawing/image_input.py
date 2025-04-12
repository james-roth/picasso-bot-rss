import cv2
from constants import (
   x_max_draw,
   x_min_draw,
   y_max_draw,
   y_min_draw,
)
import numpy as np
import tkinter as tk
from tkinter import filedialog

#=====================NOTES=====================
#This script doesn't do contour detection, it only does straightline edge detection,
#This means that it will only create a path for the segments of the image that are straight lines.
#This is useful for images that are already straight lines, such as a graph or a drawing.
#If an image does not have a relatively straight lines, it will not be able to detect them.

#All of the scaling is based on the constants file, and all waypoints are saved to a file called waypoints.txt
#The waypoints are in the format of (x0, y0, x1, y1) where (x0, y0) is the start point and (x1, y1) is the end point.
#================================================

#retrieve image and put into cv2
#open a file dialog to select an image
root = tk.Tk()
root.withdraw()  #hide the root window
img_loc = filedialog.askopenfilename(
  initialdir="./images",
  title="Select an Image",
  filetypes=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"), ("All Files", "*.*"))
)

if not img_loc:
  print("No image selected. Exiting.")
  exit()

#show the raw image
image = cv2.imread(img_loc, cv2.IMREAD_COLOR)
if image is None:
  print(f"Error: Unable to load image at {img_loc}.")
  exit()

cv2.namedWindow('raw_image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('raw_image', 600, 600)
cv2.imshow('raw_image', image)
cv2.waitKey(0)

image = cv2.imread(img_loc, cv2.IMREAD_GRAYSCALE)

if image is None:
  print(f"Error: Unable to load image at {img_loc}.")
  exit()

#gaussian blur the image to remove noise and adaptive threshold to create a binary image
blurred = cv2.GaussianBlur(image, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

#find the contours of the img
lines = cv2.HoughLinesP(
    edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10
)

#draw the raw detected lines on the image
image_with_lines = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
for line in lines:
    x0, y0, x1, y1 = line[0]
    cv2.line(image_with_lines, (x0, y0), (x1, y1), (0, 255, 0), 2)

cv2.namedWindow('base_detected_lines', cv2.WINDOW_NORMAL)
cv2.resizeWindow('base_detected_lines', 600, 600)
cv2.imshow('base_detected_lines', image_with_lines)

if lines is None:
  print("No lines found in the image.")
  exit()

print(f"Found {len(lines)} lines in the image.")

#merge similar/overlapping lines
def merge_lines(lines, threshold=15):
    merged_lines = []
    for line1 in lines:
        x0, y0, x1, y1 = line1[0]
        merged = False
        for i, (mx0, my0, mx1, my1) in enumerate(merged_lines):
            #check if the lines are close enough to merge
            if (
                abs(x0 - mx0) < threshold and abs(y0 - my0) < threshold and
                abs(x1 - mx1) < threshold and abs(y1 - my1) < threshold
            ):
                #merge the lines by averaging their endpoints
                merged_lines[i] = [
                    (x0 + mx0) // 2, (y0 + my0) // 2,
                    (x1 + mx1) // 2, (y1 + my1) // 2
                ]
                merged = True
                break
        if not merged:
            merged_lines.append([x0, y0, x1, y1])
    return merged_lines

merged_lines = merge_lines(lines)


print(f"Found {len(merged_lines)} lines after merging.")

#show base detected lines
image_with_lines = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
for line in merged_lines:
    x0, y0, x1, y1 = line
    cv2.line(image_with_lines, (x0, y0), (x1, y1), (0, 255, 0), 2)

cv2.namedWindow('merged_lines', cv2.WINDOW_NORMAL)
cv2.resizeWindow('merged_lines', 600, 600)
cv2.imshow('merged_lines', image_with_lines)

#autoscale contours to fit within the max and min drawing values
def scale_point(x, y, width, height, x_min, x_max, y_min, y_max):
    x_scaled = x_min + (x / width) * (x_max - x_min)
    y_scaled = y_min + (1 - y / height) * (y_max - y_min)  #flip y-axis to have 0,0 at bottom left
    return int(x_scaled), int(y_scaled)

height, width = image.shape
scaled_lines = []
for line in merged_lines:
    x0, y0, x1, y1 = line
    scaled_lines.append((
        scale_point(x0, y0, width, height, x_min_draw, x_max_draw, y_min_draw, y_max_draw),
        scale_point(x1, y1, width, height, x_min_draw, x_max_draw, y_min_draw, y_max_draw)
    ))

print(f"Found {len(scaled_lines)} scaled line segments to write to waypoints.")

#after we got all of the scaling, let's put the lines in order of an optimal path for drawing
#(using a greedy approach to find the closest line to the current line)
def order_lines(lines):
    ordered_lines = []
    remaining_lines = lines[:]
    drawn_lines = set()
    
    #start with the first line
    current_line = remaining_lines.pop(0)
    ordered_lines.append(current_line)
    drawn_lines.add(current_line)
    drawn_lines.add((current_line[1], current_line[0]))  #add the reverse line to the set

    while remaining_lines:
        #find the closest line to the current line's endpoint
        closest_line = None
        min_distance = float('inf')
        reverse_line = False  #flag to indicate if the closest line needs to be reversed

        for line in remaining_lines:
            #skip the lines if its already been drawn
            if line in drawn_lines or (line[1], line[0]) in drawn_lines:
                continue

            #calculate distances from the current line's endpoint to both endpoints of the candidate line
            distance_to_start = np.linalg.norm(np.array(current_line[1]) - np.array(line[0]))
            distance_to_end = np.linalg.norm(np.array(current_line[1]) - np.array(line[1]))

            #choose the smaller distance
            if distance_to_start < min_distance:
                min_distance = distance_to_start
                closest_line = line
                reverse_line = False
            if distance_to_end < min_distance:
                min_distance = distance_to_end
                closest_line = line
                reverse_line = True

        #if a closest line is found, add it to the ordered list
        if closest_line:
            if reverse_line:
                #reverse the closest line to connect it properly
                closest_line = (closest_line[1], closest_line[0])
            ordered_lines.append(closest_line)

            #mark both directions of the line as drawn
            drawn_lines.add(closest_line)
            drawn_lines.add((closest_line[1], closest_line[0]))

            current_line = closest_line
            if reverse_line:
                #if the reverse line was used, remove the original line from remaining lines (re-reverse)
                remaining_lines.remove((closest_line[1], closest_line[0]))
            else:
                remaining_lines.remove(closest_line)
        else:
            #if no nearby line exists, pick up the pen and start with the next unconnected line
            current_line = remaining_lines.pop(0)
            ordered_lines.append(current_line)

    return ordered_lines

ordered_lines = order_lines(scaled_lines)

# Write the waypoints to a file (x0, y0, x1, y1)
with open("waypoints.txt", "w") as f:
    for line in ordered_lines:
        (x0, y0), (x1, y1) = line
        f.write(f"{x0},{y0},{x1},{y1}\n")

#show the scaled straight-line segments and the order they will be drawn in
scaled_image = np.zeros((y_max_draw - y_min_draw, x_max_draw - x_min_draw, 3), dtype=np.uint8)
for i, line in enumerate(ordered_lines):
  (x0, y0), (x1, y1) = line
  #draw directional line
  cv2.arrowedLine(scaled_image, (x0, y0), (x1, y1), (0, 255, 0), 1, tipLength=0.1)
  #put a label in the middle of the arrow to show the order of the lines
  mid_x = (x0 + x1) // 2
  mid_y = (y0 + y1) // 2
  cv2.putText(scaled_image, str(i+1), (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

cv2.namedWindow('scaled_straightline_segments', cv2.WINDOW_NORMAL)
cv2.resizeWindow('scaled_straightline_segments', x_max_draw, y_max_draw)

cv2.imshow('scaled_straightline_segments', scaled_image)

cv2.waitKey(0)
cv2.destroyAllWindows()