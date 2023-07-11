import cv2 as cv
import numpy as np
import argparse

def show(img):
    cv.imshow('', img)
    if cv.waitKey(0) == ord('q'):
        cv.destroyAllWindows()

def d():
    cv.destroyAllWindows()
    
def get_edges(img):
    return cv.Canny(img, 100, 200)
  
# Parse cmd-line args
parser = argparse.ArgumentParser(description='Process an image.')
parser.add_argument('image', type=str, help='Name of the image file.')
args = parser.parse_args()
image = args.image    

# Use OpenCV to read the image
img = cv.imread(image)

# Grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Do away with bg color
# * This lower range is because of some #212121 line in theme 1... probably in the other themes too
gray_lower = np.array([33,33,33])
gray_upper = np.array([35,35,35])
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

# if __name__ == '__main__':
    # main()
