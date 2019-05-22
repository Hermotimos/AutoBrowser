

import sys
import time
import pyautogui
from image_recognition import try_click_image, recognize_number

sys.setrecursionlimit(100)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True
WIDTH, HEIGHT = pyautogui.size()

IMG_flag_CH = '.\\images\\vpn_imgs\\IMG_flag_CH.png'
IMG_flag_CAeast = '.\\images\\vpn_imgs\\IMG_flag_CAeast.png'

def click_flag():
    if pyautogui.locateOnScreen(IMG_flag_CAeast, 2, grayscale=True, region=(0.5 * WIDTH, 0, WIDTH, HEIGHT)):
        try_click_image(IMG_flag_CAeast)

click_flag()