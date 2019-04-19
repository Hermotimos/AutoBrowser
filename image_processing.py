"""
This module contains functions for recognition of meaningful site features and clicking them.

recognize_number(): Returns number recognized at specific spot or 0 if not recognized.
try_click_image(): calls click_image() - which clicks image specified via file path -
                    recursively, until success or until recursion limit is met.
"""

import sys
import pyautogui

sys.setrecursionlimit(100)

nowe_0 = '.\\images\\nowe_0.png'
nowe_1 = '.\\images\\nowe_1.png'
nowe_2 = '.\\images\\nowe_2.png'
nowe_3 = '.\\images\\nowe_3.png'
nowe_4 = '.\\images\\nowe_4.png'
nowe_5 = '.\\images\\nowe_5.png'
nowe_6 = '.\\images\\nowe_6.png'
nowe_7 = '.\\images\\nowe_7.png'
nowe_8 = '.\\images\\nowe_8.png'
nowe_9 = '.\\images\\nowe_9.png'
nowe_10 = '.\\images\\nowe_10.png'
nowe_numbers = (nowe_0, nowe_1, nowe_2, nowe_3, nowe_4, nowe_5, nowe_6, nowe_7, nowe_8, nowe_9, nowe_10)


def recognize_number():
    """Return number 0-10 for the number present at position 'Nowe', or 0 if not recognized.

    If image wasn't recognized returns 0.
    This allows click_back_n_times() in browsing_flow.py to perform in a minimalistic way, which may be then corrected.
    """
    recognized = 0
    for num, image in enumerate(nowe_numbers):
        if pyautogui.locateOnScreen(image):
            recognized = num
            break
    return recognized


def try_click_image(image_file, clicks=1, interval=0.0):
    """Try call click_image() recursively until it succeeds.

    Parameters
    ----------
        image_file (str): String representation of path to image file.
        clicks (int): Number of clicks to perform.
        interval (float): Time between clicks.

    Raises
    ------
        After recursion limit is exhausted RecursionError is raised. This is handled in main.py module.
    """
    try:
        click_image(image_file, clicks=clicks, interval=interval)
    except TypeError:
        try_click_image(image_file,  clicks=clicks, interval=interval)


def click_image(image_file, clicks, interval):
    """Recognize image on screen and click it.

    Parameters
    ----------
        image_file (str): String representation of path to image file.
        clicks (int): Number of clicks to perform.
        interval (float): Time between clicks.

    Raises
    ------
        If image is not recognized on screen TypeError is raised. This is handled by try_click_image().
    """
    location = pyautogui.locateOnScreen(image_file)
    center = pyautogui.center(location)
    pyautogui.click(center[0], center[1], clicks=clicks, interval=interval, duration=0.5)
