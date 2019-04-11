from movement_and_clicks_v2 import *
import datetime
from reporting import ParsingReport

report = ParsingReport()


def start_browsing():
    if report.write_report(determine_startpoint):
        report.write_report(scrolldown_startpage)
        report.write_report(click_search)
    report.write_report(set_strony)


def browse_pages(pages_to_browse):

    def browse_one_page():
        report.write_report(await_blueline)
        report.write_report(actively_check_list_site)
        report.write_report(click_start)
        report.write_report(switch_window_when_done)
        new_items = report.write_report(click_back_n_times)
        report.write_report(actively_check_list_site)
        report.write_report(click_next)
        return new_items

    new_count = 0
    pages_browsed = 1

    while pages_to_browse > 0:
        print('{}'.format(str(pages_browsed)))

        new_per_page = browse_one_page()

        new_count += new_per_page
        pages_browsed += 1
        pages_to_browse -= 1
        print('\t' * 12, '+{}/[{}]'.format(new_per_page, new_count))

    return new_count


def finish_browsing(new_items):
    now = datetime.datetime.now().strftime('%H.%M')
    last_page = pyautogui.screenshot()
    last_page.save('C:\\Users\\Lukasz\\Desktop\\recent__{}.jpg'.format(now))
    print('-'*20, '\nFinished: {}\nNew: {}'.format(now, new_items))
