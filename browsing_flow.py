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
from report_class import BrowsingReport
from movement_and_clicks import determine_startpoint, click_status_and_search, set_strony, \
                                   await_blueline, click_start, switch_window_when_done, click_back_n_times, \
                                   actively_check_list_site, click_next
report = BrowsingReport()


def main_flow(num_pages=0, shutdown=None):
    """Perform browsing flow.

    Asks user number of pages and shutdown mode, then follows to browsing.
    Firstly, browsing is started either from main page or from any result page; result page is reached.
    Secondly, one page is browsed at a time with possible 0-10 downloads until page limit set by user is reached.
    Thirdly, a screen shot and a report are saved into 'reports' directory and system is shut down if requested.

    All actions of Step 2 are performed within report_function() and report_non_function() methods of BrowsingReport
    so that they are printed out as log and added to 'report' instance of BrowsingReport created in this module.

    Raises
    ------
    In case of RecursionError within any of lower modules functions, recalibration is performed.
        This is a save measure: program goes back to start_browsing() phase to possibly unfreeze the page.
    In case of FailSafeException the action is included into report and program terminates.

    Todo: num_pages should be class so that it's modified and if passed down in case recalibration, it's modified value
          is passed down.

    Parameters
    ----------
    num_pages (int): Received via user input when main_flow() is called first time; then passed down by recursive calls.
    shutdown (str): Received via user input when main_flow() is called first time; then passed down by recursive calls.
    """
    if num_pages == 0:
        num_pages = ask_number_pages()
    if shutdown is None:
        shutdown = ask_shutdown()

    try:
        start_browsing()
        do_browsing(num_pages)
    except RecursionError:
        print('\nPROGRAM RECALIBRATION')
        do_browsing(num_pages)                      # Experimentally
    except pyautogui.FailSafeException:
        now = datetime.datetime.now().strftime('%H:%M:%S')
        print('\n[{}] FAILSAFE-ESCAPED.'.format(now))
        report.report_non_function('\n[{}] FAILSAFE-ESCAPED.'.format(now))
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
    report.report_function(set_strony)
    report.report_function(click_back_n_times())
    start_point = report.report_function(determine_startpoint)
    if start_point == 1:
        report.report_function(click_status_and_search)
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
        report.report_function(await_blueline)
        report.report_function(actively_check_list_site)
        report.report_function(click_start)
        report.report_function(switch_window_when_done)
        new_items = report.report_function(click_back_n_times)
        report.report_function(actively_check_list_site)
        report.report_function(click_next)
        return new_items

    pages_to_browse = (n for n in range(1, number_of_pages + 1))
    new_sum_total = 0

    for page in pages_to_browse:
        report.report_non_function(f'\n{str(page)}\n')
        new_per_page = browse_one_page()
        new_sum_total += new_per_page
        report.report_non_function('\n{}+{}/[{}]'.format('\t' * 5, new_per_page, new_sum_total))


def create_browsing_report():
    """Create directory 'reports' if doesn't exist, save screen shot and browsing report to files."""
    if 'reports' not in os.listdir('.') or not os.path.isdir('reports'):
        os.mkdir('reports')
    now = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M')

    last_page = pyautogui.screenshot()
    last_page.save(f'.\\reports\\{now}__screenshot.jpg')

    report_file = open(f'.\\reports\\{now}__report.txt', mode='w')
    report_file.write(report.__repr__())
