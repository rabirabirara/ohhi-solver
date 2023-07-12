import cv2 as cv
import numpy as np
import argparse
from math import sqrt

def show(img):
    cv.namedWindow("window", cv.WINDOW_NORMAL)
    cv.resizeWindow("window", 1280, 720)
    cv.imshow("window", img)
    if cv.waitKey(0) == ord("q"):
        cv.destroyAllWindows()


def d():
    cv.destroyAllWindows()


def get_edges(img):
    return cv.Canny(img, 100, 200)

# Parse cmd-line args
parser = argparse.ArgumentParser(description="Process an image.")
parser.add_argument("image", type=str, help="Name of the image file.")
args = parser.parse_args()
image = args.image

# Use OpenCV to read the image
img = cv.imread(image)

# Grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Do away with bg color
# * This lower range is because of some #212121 line in theme 1... probably in the other themes too
gray_lower = np.array([33, 33, 33])
gray_upper = np.array([35, 35, 35])
gray_mask = cv.bitwise_not(cv.inRange(img, gray_lower, gray_upper))
no_bg = cv.bitwise_and(img, img, mask=gray_mask)

# Do away with white text
# ! Can't really do this because of unclean edges.
# white_lower = np.array([240,240,240])
# white_upper = np.array([255,255,255])
# white_mask = cv.bitwise_not(cv.inRange(img, white_lower, white_upper))
# no_text = cv.bitwise_and(no_bg, no_bg, mask=white_mask)

# Edge detection on colored image will yield the bottom bezel lines, this can be used to detect where the filled squares are.
edges = get_edges(no_bg)

# Find contours
contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

board_contours = []

# Filter contours by area, shape, aspect_ratio, hierarchy
for contour in contours:
    area = cv.contourArea(contour)
    if area == 0.0 or area < 2000:
        continue
    
    # Perimeter-Area relation: https://link.springer.com/chapter/10.1007/978-1-4899-2124-6_12
    # perimeter = cv.arcLength(contour, True)
    # ratio = perimeter / sqrt(area)
    # ratio should be around 4 for a square
    # if not 3.8 < ratio < 4.1:
        # pass (see below)
    
    # Aspect ratio filtering
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = float(w) / h
    if not 0.97 < aspect_ratio < 1.03:
        continue
    
    cv.drawContours(img, [contour], 0, (0,255,0), 2)
    board_contours.append(contour)

board = cv.drawContours(img, board_contours, -1, (0,255,0), 2)
# weird = cv.drawContours(img, weird_contours, -1, (0,255,0), 2)


# cv.drawContours(img, contours, -1, (0,255,0), 3)

# if __name__ == '__main__':
# main()
