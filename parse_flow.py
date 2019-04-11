from movement_and_clicks_v2 import *
import datetime
from reporting import call_and_report


def start_browsing():
    if call_and_report(determine_startpoint):
        call_and_report(scrolldown_startpage)
        call_and_report(click_search)
    call_and_report(set_strony)


def browse_pages(pages_to_browse):

    def browse_one_page():
        call_and_report(await_blueline)
        call_and_report(actively_check_list_site)
        call_and_report(click_start)
        call_and_report(switch_window_when_finished)
        new_items = call_and_report(click_back_n_times)
        call_and_report(actively_check_list_site)
        call_and_report(click_next)
        return new_items

    new_count = 0
    pages_browsed = 1

    while pages_to_browse > 0:
        print('{}'.format(str(pages_browsed)))

        new_per_page = browse_one_page()

        new_count += new_per_page
        pages_browsed += 1
        pages_to_browse -= 1
        print('\t' * 15, '+{}/[{}]'.format(new_per_page, new_count))

    return new_count


def finish_browsing(new_items):
    now = datetime.datetime.now().strftime('%H.%M')
    last_page = pyautogui.screenshot()
    last_page.save('C:\\Users\\Lukasz\\Desktop\\recent__{}.jpg'.format(now))
    print('-'*20, '\nFinished: {}\nNew: {}'.format(now, new_items))