"""
This module defines class BrowsingReport which serves both as log and as report.
"""

import time


class BrowsingReport:
    def __init__(self):
        self.report = ''

    def __repr__(self):
        return self.report

    def write_report(self, called_function):
        timer = time.time()

        start_time = '[{}] '.format(time.strftime('%H:%M:%S'))
        self.report += start_time
        print(start_time, end='')

        function_name = '{:25}'.format(called_function.__repr__().split()[1])
        self.report += function_name
        print(function_name, end='')

        back_n_times = ''
        returned_value = called_function()
        if 'click_back_n_times' in function_name:
            back_n_times = '{:3}'.format(str(1 + returned_value) + 'x')
        self.report += back_n_times
        print(back_n_times, end='')

        elapsed = '\t{:-3}s\t'.format(round(time.time() - timer))
        self.report += elapsed
        print(elapsed)

        return returned_value
