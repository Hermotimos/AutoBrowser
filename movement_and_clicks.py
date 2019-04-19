import sys
import pyautogui
import time
from image_processing import click_image, recognize_number

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
    if pyautogui.locateOnScreen(IMG_STATUS, 1):
        return 1
    elif pyautogui.locateOnScreen(IMG_LISTA, 1):
        return 2
    elif pyautogui.locateOnScreen(IMG_NASTEPNA, 1) or pyautogui.locateOnScreen(IMG_NASTEPNA_2, 1):
        return 3
    else:
        pyautogui.scroll(7000)
        determine_startpoint()


def click_status_and_scrolldown():
    click_image(IMG_STATUS)
    pyautogui.scroll(-7000)


def click_search(): click_image(IMG_SZUKAJ)


def set_strony():
    click_image(IMG_NROSTAT)
    pyautogui.move(0, 20)
    pyautogui.click()
    pyautogui.press('delete', presses=5)
    pyautogui.typewrite('1')


# ELEMENTS of browse_pages()
def await_blueline():
    time.sleep(1)
    if pyautogui.locateOnScreen(IMG_BLUELINE, 60):
        pass
    elif pyautogui.locateOnScreen(IMG_BLUELINE_2, 1):       # TODO not tested so far
        pass
    else:
        click_image(IMG_BACK)


def click_start():
    if pyautogui.locateOnScreen(IMG_START_BLACK, 30):
        click_image(IMG_START_BLACK)
    else:
        click_image(IMG_BACK)
        click_start()


def switch_window_when_done():
    if pyautogui.locateOnScreen(IMG_NOWE_DONE, 60):
        click_image(IMG_WYSZUKIWARKA)
    elif pyautogui.locateOnScreen(IMG_WYSZUKIWARKA_2, 1):
        pass
    else:
        switch_window_when_done()


def click_back_n_times():
    new = recognize_number()
    n_times = new + 1
    click_image(IMG_BACK, clicks=n_times, interval=0.5)
    return new


def actively_check_list_site():                             # todo rethink this one: maybe use click_start in else
    if pyautogui.locateOnScreen(IMG_LISTA, 15):
        click_image(IMG_LISTA)
    else:
        pyautogui.locateOnScreen(IMG_BACK)
        pyautogui.move(0, 30)
        pyautogui.scroll(7000)
        if pyautogui.locateOnScreen(IMG_LISTA, 15):
            click_image(IMG_LISTA)
        else:
            click_image(IMG_BACK)
            actively_check_list_site()


def click_next():
    pyautogui.scroll(-7000)
    if pyautogui.locateOnScreen(IMG_NASTEPNA, 2):
        click_image(IMG_NASTEPNA)
    elif pyautogui.locateOnScreen(IMG_NASTEPNA_2, 2):
        click_image(IMG_NASTEPNA_2)
    else:
        click_next()
