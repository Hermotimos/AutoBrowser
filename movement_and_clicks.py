"""
This module defines functions that react to site features/events based on their recognition on screen.

Site features/events are represented by constants IMG_LISTA, IMG_STATUS etc., which contain paths to image files.
Functions in this module react to these features/events. These reactions are building blocks of browsing_flow.py.

There are two functions in browsing_flow.py that use functions from this module:

1) start_browsing() uses following functions:

determine_startpoint():
click_status_and_search():
set_strony():


2) do_browsing() uses following functions:

await_blueline():
click_start():
switch_window_when_done():
click_back_n_times():
actively_check_list_site():
click_next():

"""


import sys
import pyautogui
import time
from image_processing import try_click_image, recognize_number

sys.setrecursionlimit(100)
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

IMG_LISTA = '.\\images\\IMG_LISTA.png'
IMG_STATUS = '.\\images\\IMG_STATUS.png'
IMG_SZUKAJ = '.\\images\\IMG_SZUKAJ.png'
IMG_NROSTAT = '.\\images\\IMG_NROSTAT.png'
IMG_BLUELINE = '.\\images\\IMG_BLUELINE.png'
IMG_BLUELINE_2 = '.\\images\\IMG_BLUELINE_2.png'
IMG_BACK = '.\\images\\IMG_BACK.png'
IMG_START_BLACK = '.\\images\\IMG_START_BLACK.png'
IMG_NOWE_DONE = '.\\images\\IMG_NOWE_DONE.png'
IMG_WYSZUKIWARKA = '.\\images\\IMG_WYSZUKIWARKA.png'
IMG_WYSZUKIWARKA_2 = '.\\images\\IMG_WYSZUKIWARKA_2.png'
IMG_NASTEPNA = '.\\images\\IMG_NASTEPNA.png'
IMG_NASTEPNA_2 = '.\\images\\IMG_NASTEPNA_2.png'


# ELEMENTS OF start_browsing()
def determine_startpoint():
    """Determine if current page is the starting page or the browsing page (up or down) based on distinguishing images.
    Return code 1, 2, or 3 accordingly.
    """
    if pyautogui.locateOnScreen(IMG_STATUS, 1):
        return 1
    elif pyautogui.locateOnScreen(IMG_LISTA, 1):
        return 2
    elif pyautogui.locateOnScreen(IMG_NASTEPNA, 1) or pyautogui.locateOnScreen(IMG_NASTEPNA_2, 1):
        return 3
    else:
        pyautogui.scroll(7000)
        determine_startpoint()


def click_status_and_search():
    """Click location 'Status' on starting page, scroll down and click 'Szukaj'."""
    try_click_image(IMG_STATUS)
    pyautogui.scroll(-7000)
    try_click_image(IMG_SZUKAJ)


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


# ELEMENTS of do_browsing()
def await_blueline():
    """Wait until blue line indicating list of records is visible.

    This function ensures that program stops until another page of records is loaded.
    Recognition is based on the presence of blue line characteristic of the record page.
    The line can come in two shades, of which one is more common.
    Waiting time for loading is set to 60 secs, if the first variant is absent, checks second variant in 1 sec.

    If neither of blue line variants is visible, clicks 'back' button, as this usually unfreezes page hung by loading.
    """
    time.sleep(1)
    if pyautogui.locateOnScreen(IMG_BLUELINE, 60):
        pass
    elif pyautogui.locateOnScreen(IMG_BLUELINE_2, 1):
        pass
    else:
        try_click_image(IMG_BACK)


def click_start():
    """Click 'Start' button to start downloading records.

    Waits 30 secs until 'Start' button is visible in inactive mode (black) and clicks it.

    If the button is not visible after 30 secs, clicks 'back' button, as this usually unfreezes page hung by loading.
    Then function recursively calls itself.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    if pyautogui.locateOnScreen(IMG_START_BLACK, 30):
        try_click_image(IMG_START_BLACK)
    else:
        try_click_image(IMG_BACK)
        click_start()


def switch_window_when_done():
    """Wait until downloading is done and click at location 'Wyszukiwarka' to switch back to searching tab.

    Downloading usually takes up to 20 secs, however freezes occur frequently.
    Function waits 60 secs before it tests the possibility, that the right tab is already there.
    If not, function calls itself recursively.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    if pyautogui.locateOnScreen(IMG_NOWE_DONE, 20):
        try_click_image(IMG_WYSZUKIWARKA)
    elif pyautogui.locateOnScreen(IMG_WYSZUKIWARKA_2, 1):
        pass
    else:
        switch_window_when_done()


def click_back_n_times():
    """Click 'go back' button once plus once per each record page loaded during download.

    Clicking 'go back' once is always needed to return from start page to record page.
    For every downloaded record another time of 'go back' is needed to reach record page.
    Function uses recognize_number() to identify number of records downloaded and computes sum of 'go backs'.

    Returns
    -------
        int: Number of new records. This is then used by BrowsingReport class for running total of downloads.
    """
    new = recognize_number()
    n_times = new + 1
    try_click_image(IMG_BACK, clicks=n_times, interval=0.5)
    return new


def actively_check_list_site():
    """Waits until records site is visible.

    If the site is not visible after 15 secs, clicks 'back' button, as this usually unfreezes page hung by loading.
    Then moves cursor beneath 'back' button and scrolls up in case it landed at the bottom of page.
    Then function recursively calls itself.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    if pyautogui.locateOnScreen(IMG_LISTA, 15):
        try_click_image(IMG_LISTA)
    else:
        pyautogui.locateOnScreen(IMG_BACK)
        pyautogui.move(0, 30)
        pyautogui.scroll(7000)
        if pyautogui.locateOnScreen(IMG_LISTA, 15):
            try_click_image(IMG_LISTA)
        else:
            try_click_image(IMG_BACK)
            actively_check_list_site()


def click_next():
    """Scroll down and click 'nastepna' to go to next page.

    Site feature 'nastepna' come in two shades of blue depending on number of pages already browsed.
    It changes to darker blue after ca. 200.
    If neither is visible, function recursively calls itself.

    Raises
    ------
        If recursion limit is exhausted RecursionError is raised. This enables main.py module to recalibrate program.
    """
    pyautogui.scroll(-7000)
    if pyautogui.locateOnScreen(IMG_NASTEPNA, 2):
        try_click_image(IMG_NASTEPNA)
    elif pyautogui.locateOnScreen(IMG_NASTEPNA_2, 2):
        try_click_image(IMG_NASTEPNA_2)
    else:
        click_next()
