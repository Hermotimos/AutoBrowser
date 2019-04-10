import sys
import pyautogui
import datetime

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


def recognize_number(guess=0):
    try:
        assert pyautogui.locateOnScreen(nowe_numbers[guess])
        return guess
    except AssertionError:
        guess += 1
        if guess < 11:
            return recognize_number(guess)
        else:
            print('{}: Number at position "Nowe" not recognized'.format(datetime.datetime.now().strftime('%H:%M:%S')))
            return 0


def try_click_image(image_file, clicks=1, interval=0.0):
    try:
        click_image(image_file, clicks=clicks, interval=interval)
    except TypeError:
        try_click_image(image_file,  clicks=clicks, interval=interval)


def click_image(image_file, clicks, interval):
    location = pyautogui.locateOnScreen(image_file)
    center = pyautogui.center(location)
    pyautogui.click(center[0], center[1], clicks=clicks, interval=interval, duration=0.5)


# prototype:
# def try_go_to_image(image_file, err_cnt=0):
#     name = image_file[9:].split('.')[0]
#     now = datetime.datetime.now().strftime('%H:%M:%S')
#     try:
#         if err_cnt == 0:
#             print('[{}] do: {:20} {:5}'.format(now, name, err_cnt), end='')
#         go_to_image(image_file)
#     except TypeError:
#         err_cnt += 1
#         print('{}[{}] do: {:20} {:5}'.format('\b'*100, now, name, err_cnt), end='')
#         try_go_to_image(image_file, err_cnt)
#
#
# def go_to_image(image_file):
#     location = pyautogui.locateOnScreen(image_file)
#     center = pyautogui.center(location)
#     pyautogui.moveTo(center[0], center[1])

