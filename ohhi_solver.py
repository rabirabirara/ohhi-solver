import cv2
import pyautogui
import sys
import time

# Do board detection here

CURRENT_THEME = "theme1"

def detect_board():
    print("Detecting board:")
    blanks = map(pyautogui.center, list(pyautogui.locateAllOnScreen(f"img/{CURRENT_THEME}/tile-0.png")))
    ones = map(pyautogui.center, list(pyautogui.locateAllOnScreen(f"img/{CURRENT_THEME}/tile-1.png")))
    twos = map(pyautogui.center, list(pyautogui.locateAllOnScreen(f"img/{CURRENT_THEME}/tile-2.png")))
    print(list(blanks))
    print(list(ones))
    print(list(twos))
    
    


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
