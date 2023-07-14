import cv2 as cv
import pyautogui
import numpy as np
import sys
import time
import subprocess
import ast

import detect_board as detect
import gen_constraints as gen_cons

# Put path of the compiled executable of gnu-ohhi.pl
EXECUTABLE = "build\\gnu-ohhi.exe"
CURRENT_THEME = "theme1"


def print_neat(lst):
    for l in lst:
        print(l)


def is_within(n1, n2, tol):
    return abs(n1 - n2) < tol


def is_dupe_point(a, b):
    return is_within(a.x, b.x, 5) and is_within(a.y, b.y, 5)


def deduped_points(points):
    final = []
    for i in range(len(sorted(points, key=lambda k: [k[0], k[1]]))):
        no_dupes = True
        # Go forward, if there are duplicates don't add this.
        for j in range(i + 1, len(points)):
            if is_dupe_point(points[i], points[j]):
                no_dupes = False
                break
            else:
                print(f"not dupe: {points[i]}, {points[j]}")
        if no_dupes:
            final.append(points[i])
    return final


def main():
    print("Script started. Detecting active play:")
    then = time.time()
    found = False
    # Do this only for 10 seconds
    while (time.time() - then) < 10.0:
        print(time.time() - then)
        # look for board by looking for history button
        # ! Docs say that this throws if not found but that is bullshit. It returns None.
        try:
            loc = pyautogui.locateCenterOnScreen(
                f"img/{CURRENT_THEME}/history.png", grayscale=True, confidence=0.95
            )
            if loc is not None:
                found = True
                break
            else:
                time.sleep(0.5)
        except pyautogui.ImageNotFoundException:
            time.sleep(0.5)
        except Exception as e:
            raise e

    if not found:
        print("Did not find active game in 10 seconds. Quitting.")
        # not even in game state, just quit
        return 1

    # Found. Perform the board detection
    print("Game state is active (found history icon!).")
    print(loc)

    # Screenshot the game
    screenshot = pyautogui.screenshot()
    np_img = np.array(screenshot)
    cv_img = cv.cvtColor(np_img, cv.COLOR_RGB2BGR)

    # coords is 1d list of tuples
    (n, spec, coords) = detect.img_to_spec_n_coords(cv_img)

    constraints_str = gen_cons.spec_to_constraints(spec)

    # Call the prolog subroutine
    result = subprocess.check_output([EXECUTABLE, str(n), constraints_str], text=True)

    # Example output:
    """
    [...]
    [...]
    """
    # Note the lack of commas and outer braces. We must add those back in.

    # Interpret the string as python instead of parsing it.
    board_str = "[" + ",".join(result.splitlines()) + "]"
    board = ast.literal_eval(board_str)

    detect.show_2d_board([[x+1 for x in l] for l in board])

    # Clicking: have the script actually click as appropriate on the coords according to the solution.
    # 0 means left click, 1 means right click.
    for i in range(n):
        for j in range(n):
            click_type = "right" if board[i][j] else "left"
            (x, y) = coords[n * i + j]
            pyautogui.click(x=x, y=y, button=click_type, duration=0.0)

    print("Script completed.")


if __name__ == "__main__":
    main()
