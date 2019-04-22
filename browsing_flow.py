"""
This module defines functions for browsing flow.

This is achieved in main.py module by calling following 3 functions consecutively:
start_browsing():
do_browsing():
finish_browsing():

Firstly, browsing is started either from main page or from any result page.
One page is browsed at a time with possible 0-10 downloads.
"""

import time
import pyautogui
from report_class import BrowsingReport
from movement_and_clicks import determine_startpoint, click_status_and_search, set_strony, \
                                   await_blueline, click_start, switch_window_when_done, click_back_n_times, \
                                   actively_check_list_site, click_next
report = BrowsingReport()


def start_browsing():
    """Set number of pages browsed at a time to 1 and reach next records page according to the determined current page.

    If current page is start page, clicks 'Szukaj' (Search) button to reach first records page.
    If current page is records page, do nothing (let do_browsing() overtake).
    """
    report.write_report(set_strony)
    start_point = report.write_report(determine_startpoint)
    if start_point == 1:
        report.write_report(click_status_and_search)
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
        report.write_report(await_blueline)
        report.write_report(actively_check_list_site)
        report.write_report(click_start)
        report.write_report(switch_window_when_done)
        new_items = report.write_report(click_back_n_times)
        report.write_report(actively_check_list_site)
        report.write_report(click_next)
        return new_items

    pages_to_browse = (n for n in range(1, number_of_pages + 1))
    new_sum_total = 0

    for page in pages_to_browse:
        print('{}'.format(page))
        new_per_page = browse_one_page()
        new_sum_total += new_per_page
        print('\t' * 12, '+{}/[{}]'.format(new_per_page, new_sum_total))


def finish_browsing():
    last_page = pyautogui.screenshot()
    last_page.save('.\\reports\\recent__{}.jpg'.format(time.strftime('%H.%M')))

    # todo create dir if not exists
    # todo write report to file
