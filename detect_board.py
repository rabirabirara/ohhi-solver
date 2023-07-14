import cv2 as cv
import numpy as np
import argparse
from math import sqrt, floor

# How to use:
# Import this file, and then pass the image (as numpy array) to run(img). It should return a board or throw exception.

map_bgr = {
    0: [[30, 50], [30, 50], [30, 50]],  # gray
    1: [[35, 55], [55, 85], [165, 210]],  # red
    2: [[165, 205], [150, 180], [35, 55]],  # blue
}


# Convenience, open an image.
def show(img):
    cv.namedWindow("window", cv.WINDOW_NORMAL)
    cv.resizeWindow("window", 1280, 720)
    cv.imshow("window", img)
    if cv.waitKey(0) == ord("q"):
        cv.destroyAllWindows()


def flat_to_spec(flat_board):
    n = int(sqrt(len(flat_board)))
    # Converts a 1d_board to a series of lines - a specification for a board.
    board_spec = ""
    for i in range(n):
        for j in range(n):
            color = flat_board[n * i + j]
            if color != 0:
                board_spec += f"{i},{j},{color - 1}\n"
    return board_spec


def flat_to_2d(flat_board):
    n = int(sqrt(len(flat_board)))
    return np.reshape(np.array(flat_board), (-1, n))


# Shows a 2d board (matrix)
def show_2d_board(board):
    for row in board:
        for item in row:
            match item:
                case 0:
                    print("⬛", end="")
                case 1:
                    print("🟥", end="")
                case 2:
                    print("🟦", end="")
                case _:
                    print(
                        "Invalid color in the board! Probably a None, meaning a color wasn't approximated."
                    )
        print("")


def d():
    cv.destroyAllWindows()


def get_mins_maxs(points):
    (x_min, x_max, y_min, y_max) = (100000, 0, 100000, 0)
    # points: [ [[y, x]] ... ]
    for p in points:
        x_min = min(x_min, p[0][1])
        x_max = max(x_max, p[0][1])
        y_min = min(y_min, p[0][0])
        y_max = max(y_max, p[0][0])
    return (x_min, x_max, y_min, y_max)


def between(n, low, high):
    return low < n < high


def between_t(n, arr):
    return arr[0] < n < arr[1]


def approx_color(bgr):
    (b, g, r) = bgr[0], bgr[1], bgr[2]
    gray, red, blue = map_bgr[0], map_bgr[1], map_bgr[2]
    if between_t(b, gray[0]) and between_t(g, gray[1]) and between_t(r, gray[2]):
        return 0
    if between_t(b, red[0]) and between_t(g, red[1]) and between_t(r, red[2]):
        return 1
    if between_t(b, blue[0]) and between_t(g, blue[1]) and between_t(r, blue[2]):
        return 2
    raise ValueError(f"Color not found: {bgr}")


def img_to_spec_n(img):
    flat = img_to_flat(img)
    n = int(sqrt(len(flat)))
    return (n, flat_to_spec(flat))


def img_to_spec(img):
    return flat_to_spec(img_to_flat(img))


def img_to_flat(img):
    # Do away with bg color
    # * This lower range is because of some #212121 line in theme 1... probably in the other themes too
    gray_lower = np.array([33, 33, 33])
    gray_upper = np.array([35, 35, 35])
    gray_mask = cv.bitwise_not(cv.inRange(img, gray_lower, gray_upper))
    no_bg = cv.bitwise_and(img, img, mask=gray_mask)

    # Edge detection on colored image will yield the bottom bezel lines, this can be used to detect where the filled squares are.
    edges = cv.Canny(no_bg, 100, 200)

    # Find contours
    contours, hierarchy = cv.findContours(edges, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    board_contours = []

    # Filter contours by area, shape, aspect_ratio, hierarchy
    for i in range(len(contours)):
        contour = contours[i]
        h = hierarchy[0][i]

        # Select contours with no parent (outermost)
        if h[3] != -1:
            continue

        area = cv.contourArea(contour)
        if area < 2000:
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
        if not between(aspect_ratio, 0.97, 1.03):
            continue

        # cv.drawContours(img,[contour], 0, (0,255,0), 2)
        board_contours.append(contour)

    n = floor(sqrt(len(board_contours)))
    if n * n != len(board_contours) or n % 2 == 1:
        raise ValueError(
            f"Invalid board size: n = {n} with {len(board_contours)} many squares found; check the board detection code."
        )

    # All black image in the same shape
    blk_mask = np.empty_like(img)

    squares = []

    # OPTIONAL: extract squares and mask them on img
    for c in board_contours:
        # Approximate 4-point polygons out of the contours
        epsilon = 0.02 * cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, epsilon, True)
        squares.append(approx)

        # Draw them onto a mask
        cv.fillPoly(blk_mask, [approx], (255, 255, 255))
    # Extract the interesting bits from the image using the mask (optional)
    final = cv.bitwise_and(img, blk_mask)

    flat_board = []

    # Obtain the average colors of each polygon
    # squares is in reversed order (from bottom right to top left) so reverse it
    for square in reversed(squares):
        # square: [ [[y, x]] ... ]

        # Get all the pixels in the square from the image
        (x1, x2, y1, y2) = get_mins_maxs(square)
        piece = final[x1:x2, y1:y2]

        # Take average color
        bgr_avg = np.mean(piece, axis=(0, 1))
        color = approx_color(bgr_avg)

        flat_board.append(color)

    # show_board(flat_board)

    return flat_board


def main():
    # Parse cmd-line args
    parser = argparse.ArgumentParser(description="Process an image.")
    parser.add_argument("image", type=str, help="Name of the image file.")
    args = parser.parse_args()
    image = args.image

    # Use OpenCV to read the image
    img = cv.imread(image)

    # Produce 1d board
    flat_board = img_to_flat(img)

    show_2d_board(flat_to_2d(flat_board))


if __name__ == "__main__":
    main()
