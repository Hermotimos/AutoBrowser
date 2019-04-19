import time
import pyautogui
from report_class import ParsingReport
from movement_and_clicks import determine_startpoint, click_status_and_scrolldown, click_search, set_strony, \
                                   await_blueline, click_start, switch_window_when_done, click_back_n_times, \
                                   actively_check_list_site, click_next
report = ParsingReport()


def start_browsing():
    start_point = report.write_report(determine_startpoint)
    if start_point == 1:
        report.write_report(click_status_and_scrolldown)
        report.write_report(click_search)
    elif start_point == 2:
        pass
    elif start_point == 3:
        report.write_report(click_next)
    report.write_report(set_strony)


def do_browsing(number_of_pages):

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
