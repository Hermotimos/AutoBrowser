import os
import pyautogui
import datetime
from parse_flow import start_browsing, browse_pages, finish_browsing
from settings import ask_number_pages, ask_shutdown


def main_flow(pages_to_browse):
    num_pages = pages_to_browse

    try:
        start_browsing()
        new_sum = browse_pages(num_pages)
        finish_browsing(new_sum)
    except RecursionError:
        print('\nPROGRAM RECALIBRATION')
        main_flow(num_pages)
    except pyautogui.FailSafeException:
        now = datetime.datetime.now().strftime('%H:%M:%S')
        print('\n[{}] FAILSAFE-ESCAPED.'.format(now))


pages = ask_number_pages()
ifshut = ask_shutdown()

main_flow(pages)
os.system("{}".format(ifshut))
