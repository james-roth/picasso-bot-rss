import cv2

#retrieve image and put into cv2
#TODO: maybe change this to a web url? rather than a saved image?
img_loc = input("Enter the location of the image: ")
image = cv2.imread(img_loc, cv2.IMREAD_GRAYSCALE)

#find the contours of the img
contours, heirarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#filter the contours to not include the border
height, width = image.shape
contours_filtered = []
for cnt in contours:
  border_touching = False
  for point in cnt:
    x,y = point[0]
    if x == 0 or x == width - 1 or y == 0 or y == height - 1:
      border_touching = True
      break
  if not border_touching:
    contours_filtered.append(cnt)

#only include a minimum size contour
min_contour_area = 100
contours_filtered = [cnt for cnt in contours_filtered if cv2.contourArea(cnt) > min_contour_area]

#only include "unique-enough" contours, and try a basic simplification
unique_contours = []
for c in contours_filtered:
  epsilon = 0.005 * cv2.arcLength(c, True)
  approx_contour = cv2.approxPolyDP(c, epsilon, True)

  if not any(cv2.matchShapes(approx_contour, u, 1, 0.0) < 0.01 for u in unique_contours):
    unique_contours.append(approx_contour)

#draw the contours on the img and display
image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(image_with_contours, unique_contours, -1, (0,255,0), 2)

#name and resize window
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600, 400)

cv2.imshow('image', image_with_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()


#TODO: from this point, we have to parse each contour into straight lines
#TODO: after parsing, write it into image_waypoints.txt `x0, y0, x1, y1\n`
