import datetime
import time


def call_and_report(called_function):
    start = time.time()
    print('[{}] '.format(datetime.datetime.now().strftime('%H:%M:%S')), end='')
    print('{:25}'.format(called_function.__repr__().split()[1]), end='')
    
    anyreturn = called_function()
    back_n_times = ''
    if called_function.__repr__().split()[1] == 'click_back_n_times':
        back_n_times = str(1 + anyreturn) + 'x'

    print('{:3}\t{}s\t'.format(back_n_times, round(time.time() - start)), end='')
    print('[{}] '.format(datetime.datetime.now().strftime('%H:%M:%S')))

    return anyreturn
