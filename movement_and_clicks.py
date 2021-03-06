"""
This module defines functions that react to site features/events based on their recognition on screen.

Site features/events are represented by constants IMG_LISTA, IMG_STATUS etc., which contain paths to image files.
Functions in this module react to these features/events and their malfunctions.
These reactions are building blocks of browsing_flow.py.

All functions in this moduled are decorated with log_action() decorator to produce log and report.

There are two functions in browsing_flow.py that use functions from this module:

1) start_browsing() uses following functions:
    set_strony():               Sets number of pages to be browsed for downloading.
    determine_startpoint():     Returns number representing detected current page.
    click_status_and_search():  Clicks 'Szukaj' button on start page.



2) do_browsing() uses following functions:
    actively_check_list_site(): Checks if current page is results page.
    click_start():              Clicks 'Start' button to initiate download.
    switch_window_when_done():  Goes back to search engine after download is finished.
    click_back_n_times():       Goes back n time, where n = 1 + number of pages opened during download.
    click_next():               Goes to next results page.
"""

import sys
import time
import pyautogui
from image_recognition import try_click_image, recognize_number

sys.setrecursionlimit(100)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True
WIDTH, HEIGHT = pyautogui.size()

IMG_BACK = '.\\images\\IMG_BACK.png'
# IMG_BLUELINE_1 = '.\\images\\IMG_BLUELINE_1.png'
# IMG_BLUELINE_2 = '.\\images\\IMG_BLUELINE_2.png'
IMG_BREAK = '.\\images\\IMG_BREAK.png'
IMG_LISTA = '.\\images\\IMG_LISTA.png'
IMG_NASTEPNA_1 = '.\\images\\IMG_NASTEPNA_1.png'
IMG_NASTEPNA_2 = '.\\images\\IMG_NASTEPNA_2.png'
IMG_NASTEPNA_3 = '.\\images\\IMG_NASTEPNA_3.png'
# IMG_NOT_DONE = '.\\images\\IMG_NOT_DONE.png'
IMG_NOWE_DONE = '.\\images\\IMG_NOWE_DONE.png'
IMG_NROSTAT = '.\\images\\IMG_NROSTAT.png'
IMG_START_BLACK = '.\\images\\IMG_START_BLACK.png'
IMG_START_GRAY = '.\\images\\IMG_START_GRAY.png'
IMG_STATUS = '.\\images\\IMG_STATUS.png'
IMG_STOP = '.\\images\\IMG_STOP.png'
IMG_SZUKAJ = '.\\images\\IMG_SZUKAJ.png'
IMG_WYSZUKIWARKA_1 = '.\\images\\IMG_WYSZUKIWARKA_1.png'
IMG_WYSZUKIWARKA_2 = '.\\images\\IMG_WYSZUKIWARKA_2.png'


# ELEMENTS OF start_browsing()

def set_strony():
    """Set number of pages browsed by downloading to 1.

    Clicks at location 'numer ostatniej strony' and moves 20 pixels beneath to the combo box.
    Activates the box, deletes whatever is in it and types '1' to ensure browsing of 1 page at a time.
    """
    try_click_image(IMG_NROSTAT)
    pyautogui.move(0, 20)
    pyautogui.click()
    pyautogui.press('delete', presses=5)
    pyautogui.typewrite('1')


def determine_startpoint():
    """Determine if current page is the start page or the records page. Return 1 or 2 accordingly.

    If neither can be determined function scrolls up and calls itself recursively.

    Returns
    -------
        int: Value 1 for start page, value 2 for records page.
    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    if pyautogui.locateOnScreen(IMG_STATUS, grayscale=True, region=(0, 0, 0.5 * WIDTH, HEIGHT)):
        return 1
    elif pyautogui.locateOnScreen(IMG_START_BLACK, grayscale=True, region=(0, 0, 0.5 * WIDTH, 0.5 * HEIGHT)):
        return 2
    else:
        determine_startpoint()


def click_status_and_search():
    """Click location 'Status' on start page, scroll down and click 'Szukaj'."""
    try_click_image(IMG_STATUS)
    pyautogui.scroll(-7000)
    try_click_image(IMG_SZUKAJ)


# ELEMENTS of do_browsing()

def actively_check_list_site():
    """Waits until results page is visible.

    If the site is not visible after 15 secs, clicks 'back' button, as this usually unfreezes page hung by loading.
    Then moves cursor beneath 'back' button and scrolls up in case it landed at the bottom of page.
    Then function recursively calls itself.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    if pyautogui.locateOnScreen(IMG_LISTA, 10, grayscale=True, region=(0, 0, 0.5 * WIDTH, 0.3 * HEIGHT)):
        try_click_image(IMG_LISTA)
    else:
        pyautogui.move(0, 200)
        pyautogui.click()
        pyautogui.scroll(7000)
        if pyautogui.locateOnScreen(IMG_LISTA, 10, grayscale=True, region=(0, 0, 0.5 * WIDTH, 0.3 * HEIGHT)):
            try_click_image(IMG_LISTA)
        else:
            try_click_image(IMG_BACK)
            actively_check_list_site()


def click_start():
    """Click 'Start' button to start downloading results.

    Waits 30 secs until 'Start' button is visible in inactive mode (black) and clicks it.
    If the button is not visible after 30 secs, clicks 'back' button, as this usually unfreezes page hung by loading.
    Then function recursively calls itself.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    if pyautogui.locateOnScreen(IMG_START_BLACK, 30, grayscale=True, region=(0, 0, 0.5 * WIDTH, 0.3 * HEIGHT)):
        try_click_image(IMG_START_BLACK)
    else:
        try_click_image(IMG_BACK)
        click_start()


def switch_window_when_done():
    """Wait until downloading is done and click at location 'Wyszukiwarka' to switch back to searching tab.

    Function takes 2 secs to move cursor, which creates delay before locateOnScreen() takes screen shot.
    Otherwise screen shot is often made before downloading starts, so the function fires to soon.
    Downloading usually takes up to 20 secs, however freezes occur frequently, so function calls itself recursively.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    # time.sleep(1)
    # if pyautogui.locateOnScreen(IMG_NOWE_DONE, grayscale=True, region=(0, 0, 0.5*WIDTH, 0.2*HEIGHT)):
    #     time.sleep(1)
    #     if pyautogui.locateOnScreen(IMG_NOWE_DONE, grayscale=True, region=(0, 0, 0.5*WIDTH, 0.2*HEIGHT)):
    #         if pyautogui.locateOnScreen(IMG_WYSZUKIWARKA_1, grayscale=True, region=(0, 0, 0.2 * WIDTH, 0.2 * HEIGHT)):
    #             try_click_image(IMG_WYSZUKIWARKA_1)
    #         else:
    #             try_click_image(IMG_WYSZUKIWARKA_2)
    # else:
    #     switch_window_when_done()

    # v2
    time.sleep(2)
    if pyautogui.locateOnScreen(IMG_START_GRAY, grayscale=True,region=(0, 0, 0.5*WIDTH, 0.2*HEIGHT)):
        if pyautogui.locateOnScreen(IMG_NOWE_DONE, grayscale=True, region=(0, 0, 0.5 * WIDTH, 0.2 * HEIGHT)):
            if pyautogui.locateOnScreen(IMG_WYSZUKIWARKA_1, grayscale=True, region=(0, 0, 0.2 * WIDTH, 0.2 * HEIGHT)):
                try_click_image(IMG_WYSZUKIWARKA_1)
            else:
                try_click_image(IMG_WYSZUKIWARKA_2)
    else:
        switch_window_when_done()


def click_back_n_times():
    """Click 'go back' button once plus once per each results page loaded during download.

    Clicking 'go back' once is always needed to return from start page to results page.
    For every downloaded results another time of 'go back' is needed to reach results page.
    Function uses recognize_number() to identify number of results downloaded and computes sum of 'go backs'.

    Returns
    -------
        int: Number of new results. This is then used by BrowsingReport class for running total of downloads.
    """
    new = recognize_number()
    n_times = new + 1
    if pyautogui.locateOnScreen(IMG_WYSZUKIWARKA_2, grayscale=True, region=(0, 0, 0.5 * WIDTH, 0.2 * HEIGHT)):
        try_click_image(IMG_BACK, clicks=n_times, interval=0.5)
        pyautogui.move(0, 100, duration=1)
    else:
        try_click_image(IMG_WYSZUKIWARKA_1)
        click_back_n_times()
    return new


def click_next():
    """Scroll down and click 'nastepna' to go to next page.

    Site feature 'nastepna' come in two shades of blue depending on number of pages already browsed.
    It changes to darker blue after ca. 200.
    If neither is visible, clicks 'go back' button, moves cursor over result page and recursively calls itself.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    pyautogui.scroll(-7000)
    if pyautogui.locateOnScreen(IMG_NASTEPNA_1, 2, grayscale=True, region=(0, 0.5 * HEIGHT, WIDTH, HEIGHT)):
        try_click_image(IMG_NASTEPNA_1)
    elif pyautogui.locateOnScreen(IMG_NASTEPNA_2, 2, grayscale=True, region=(0, 0.5 * HEIGHT, WIDTH, HEIGHT)):
        try_click_image(IMG_NASTEPNA_2)
    elif pyautogui.locateOnScreen(IMG_NASTEPNA_3, 2, grayscale=True, region=(0, 0.5 * HEIGHT, WIDTH, HEIGHT)):
        try_click_image(IMG_NASTEPNA_3)
    else:
        try_click_image(IMG_BREAK)
        try_click_image(IMG_BACK)
        pyautogui.move(0, 50, duration=5)
        click_next()


def click_stop_if_not_done():
    if pyautogui.locateOnScreen(IMG_STOP, 2, grayscale=True, region=(0, 0, 0.5 * WIDTH, 0.3 * HEIGHT)):
        try_click_image(IMG_STOP)
