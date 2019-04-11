from movement_and_clicks_v2 import *
import time
from reporting import ParsingReport

report = ParsingReport()


def start_browsing():
    if report.write_report(determine_startpoint):
        report.write_report(scrolldown_startpage)
        report.write_report(click_search)
    report.write_report(set_strony)


def browse_pages(number_of_pages):

    def browse_one_page():
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
