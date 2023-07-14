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

    (n, spec) = detect.img_to_spec_n(cv_img)

    constraints_str = gen_cons.spec_to_constraints(spec)

    # Call the prolog subroutine
    result = subprocess.check_output(
        [EXECUTABLE, str(n), constraints_str], text=True
    )
    
    # The output is just each list printed on a new line, so we need to 
    # make a list of lists by adding an extra pair of braces at the end.
    board_str = '[' + result.stdout + ']'
    
    # * For convenience: interpret the string as python instead of parsing it.
    board = ast.literal_eval(board_str)

if __name__ == "__main__":
    main()
