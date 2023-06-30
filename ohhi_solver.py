import cv2
import pyautogui
import sys
import time
import math

# Do board detection here

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
        for j in range(i+1, len(points)):
            if is_dupe_point(points[i], points[j]):
                no_dupes = False
                break
            else:
                print(f"not dupe: {points[i]}, {points[j]}")
        if no_dupes:
            final.append(points[i])
    return final


def detect_board():
    print("Detecting board:")
    blanks = deduped_points(
        [
            pyautogui.center(p)
            for p in pyautogui.locateAllOnScreen(
                f"img/{CURRENT_THEME}/tile-0.png",
                grayscale=True,
                confidence=0.9,
            )
        ]
    )
    ones = deduped_points(
        [
            pyautogui.center(p)
            for p in pyautogui.locateAllOnScreen(
                f"img/{CURRENT_THEME}/tile-1.png",
                grayscale=True,
                confidence=0.9,
            )
        ]
    )
    # twos = list(map(pyautogui.center, list(pyautogui.locateAllOnScreen(f"img/{CURRENT_THEME}/tile-2.png", confidence=0.98))))
    print(f"blanks: {blanks}; {len(blanks)}")
    print_neat(blanks)
    print(f"ones: {ones}; {len(ones)}")
    print_neat(ones)
    # print(f"twos: {twos}; {len(twos)}")
    # print_neat(twos)
    all = sorted(set(blanks + ones), key=lambda k: [k.x, k.y])
    if not math.log2(len(all)).is_integer():
        print(
            f"Invalid board size! Detected {len(all)} points. There should be a power of 2."
        )
    else:
        print(all)


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
    detect_board()


if __name__ == "__main__":
    main()
