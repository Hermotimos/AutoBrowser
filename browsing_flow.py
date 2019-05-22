"""
This module defines functions for browsing flow.

This is achieved in 2 steps in main() function:

Step 1: Determining modalities.
    ask_number_pages(): Asks for user input to determine number of pages to browse.
    ask_shutdown(): Asks for user input to determine, whether system should be shut down or hibernated after completion.

Step 2: Performing browsing.
    Following 3 functions are called consecutively:
    start_browsing():           Goes to first or next records page.
    do_browsing():              Browses number of pages defined by user.
    create_browsing_report():   Saves screen shot and report to files in 'reports' directory.

Todo
    Create global variable page_cnt => pages_to_browse should equal initial number minus page_cnt
    (to avoid reset by recalibration)
"""

import os
import datetime
import pyautogui
from report_classes import BrowsingReport, MyCounter
from movement_and_clicks import determine_startpoint, click_status_and_search, set_strony, click_start, \
                                switch_window_when_done, click_back_n_times, actively_check_list_site, click_next, \
                                click_stop_if_not_done

log = BrowsingReport()
page_counter = MyCounter(start_count_from=1)
item_counter = MyCounter(start_count_from=0)
recalibration_counter = MyCounter(start_count_from=0)


def main_flow():
    """Perform browsing flow.

    Asks user for number of pages and shutdown mode, then follows to browsing.
    Firstly, browsing is started either from a result page or from main page (in this case reaches first result page).
    Secondly, one page is browsed at a time with possible 0-10 downloads until page limit set by user is reached.
    Thirdly, a screen shot and a report are saved into 'reports' directory and system is shut down if requested.

    All actions of Step 2 are performed within report() and report_non_function() methods of BrowsingReport
    so that they are printed out as log and added to 'log' instance of BrowsingReport created in this module.

    Raises
    ------
    In case of RecursionError within any of lower modules functions, recalibration is performed.
        This is a save measure: program goes back to start_browsing() phase to possibly unfreeze the page.
    In case of FailSafeException the action is included into report and program terminates.

    Todo: num_pages should be class so that it's modified and if passed down in case recalibration, its modified value
          is passed down.

    Parameters
    ----------
    num_pages (int): Received via user input when main_flow() is called first time; then passed down by recursive calls.
    shutdown (str): Received via user input when main_flow() is called first time; then passed down by recursive calls.
    """
    num_pages = ask_number_pages()
    shutdown = ask_shutdown()

    try:
        start_browsing()
        do_browsing(num_pages)
    except (RecursionError, TypeError):
        print('\nPROGRAM RECALIBRATION START')
        recalibrate()
        recalibration_counter.increment()
        print('PROGRAM RECALIBRATION END')
        do_browsing(num_pages)
    except pyautogui.FailSafeException:
        now = datetime.datetime.now().strftime('%H:%M:%S')
        print('\n[{}] FAILSAFE-ESCAPED.'.format(now))
        log.report(f'\n[{now}] FAILSAFE-ESCAPED.')
    finally:
        create_browsing_report()
        os.system("{}".format(shutdown))


def ask_number_pages():
    """Ask user for number of pages to browse. If provided number is invalid, ask recursively. Return input as int."""
    num = input('Enter number of pages to browse and confirm by ENTER:\n')
    try:
        num = int(num)
        assert num > 0
        return num
    except Exception as e:
        print('ERROR:', e)
        return ask_number_pages()


def ask_shutdown():
    """Ask user if they want to shut down system after program ends. Return cmd command as str accordingly.

    Returns
    -------
        str: Returns str that is used as cmd command for shutdown. If user's input is not 's' or 'h', then empty str.
    """
    choice = input("Choose shutdown mode after program finishes:\nshutdown - s\nhibernation - h\nnone - any key\n")
    mode = ''
    if choice == 's':
        mode = "shutdown /s /t 1"
    elif choice == 'h':
        mode = "shutdown /h"
    return mode


def start_browsing():
    """Set number of pages browsed at a time to 1 and reach next records page according to the determined current page.

    If current page is start page, clicks 'Szukaj' (Search) button to reach first records page.
    If current page is records page, do nothing (let do_browsing() overtake).
    """
    log.report(set_strony)
    if log.report(determine_startpoint) == 1:
        log.report(click_status_and_search)
    else:
        pass


def do_browsing(number_of_pages):
    """Browse number of result pages chosen by user and print log with page number and downloads counters after each.

    This function calls nested function browse_one_page() in a loop, which amounts to specified number of pages.
    It prints page number before browsing each page and count of new items together with running total after each page.

    Parameters
    ----------
    number_of_pages (int): Specifies how many pages should be browsed.
    """

    def browse_one_page():
        """Browse one result page and return count of items downloaded per page."""
        log.report(actively_check_list_site)
        log.report(click_start)
        log.report(switch_window_when_done)
        new_items = log.report(click_back_n_times)
        item_counter.increment(increment_by=new_items)
        log.report(click_next)
        return new_items

    for page in range(page_counter.current(), number_of_pages + 1):
        page_counter.increment()
        log.report(f'\n{str(page)}/{number_of_pages}\n')
        new_per_page = browse_one_page()
        log.report('------\n+{}/[{}]\n'.format(new_per_page, item_counter.current()))


def recalibrate():
    log.report(click_stop_if_not_done)
    log.report(switch_window_when_done)
    log.report(click_back_n_times)


def create_browsing_report():
    """Create directory 'reports' if doesn't exist, save screen shot and browsing log to files."""

    now = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M')
    log.report(f'\n[{now}] FINISHED.')
    log.report(f'\n[{now}] {page_counter.current()} pages.')
    log.report(f'\n[{now}] {item_counter.current()} new items.')
    log.report(f'\n[{now}] {recalibration_counter.current()} recalibrations.')

    if 'reports' not in os.listdir('.') or not os.path.isdir('reports'):
        os.mkdir('reports')

    last_page = pyautogui.screenshot()
    last_page.save(f'.\\reports\\{now}__screenshot.jpg')

    report_file = open(f'.\\reports\\{now}__report.txt', mode='w')
    report_file.write(log.__repr__())
