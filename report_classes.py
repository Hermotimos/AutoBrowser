"""
This module defines class BrowsingReport which serves both as log and as report.
"""

import time


class BrowsingReport:
    """
    Its objects serve as logs printed out during program execution and as reports printed out afterwards.
    report(): serves to print out log
    __repr__(): serves to create end report, is dependant from report()
    """

    def __init__(self):
        """Create object of BrowsingReport with attribute 'log' as empty str."""
        self.session_report = ''

    def report(self, func_or_str):
        """Print as log and add to 'session_report' all info about flow functions and additional lines for formatting.

        Strings represent non-function data for report like page number or new items counter.
        For every function or str passed to this method write info to attribute session_report' and print out into log.

        For each function called with this method following data will be printed into log and added to 'session_report':
        - execution starting time
        - function name
        - execution time

        Example
        -------
            [17:38:59] set_strony               	  3s
            [17:39:02] determine_startpoint     	  5s

            1
            [17:39:07] actively_check_list_site 	  2s
            [17:39:09] click_start              	  1s
            [17:39:10] switch_window_when_done  	  5s
            [17:39:15] click_back_n_times       2x 	  3s
            [17:39:18] actively_check_list_site 	  2s
            [17:39:19] click_next               	  3s

                                +1/[1]
            2
            [17:39:22] actively_check_list_site 	  3s
            (...)
        """
        if isinstance(func_or_str, str):
            self.session_report += func_or_str
            print(func_or_str, end='')
        else:
            function = func_or_str
            timer = time.time()

            start_time = '[{}] '.format(time.strftime('%H:%M:%S'))
            self.session_report += start_time
            print(start_time, end='')

            function_name = '{:25}'.format(function.__repr__().split()[1])
            self.session_report += function_name
            print(function_name, end='')

            back_n_times = ''
            returned_value = function()
            if 'click_back_n_times' in function_name:
                back_n_times = '{:3}'.format(str(1 + returned_value) + 'x')
            self.session_report += back_n_times
            print(back_n_times, end='')

            elapsed = '\t{:-3}s\t'.format(round(time.time() - timer))
            self.session_report += elapsed + '\n'
            print(elapsed)

            return returned_value

    def __repr__(self):
        """Return whole object."""
        return self.session_report


class MyCounter:
    def __init__(self, start_count_from=0):
        self.number = start_count_from

    def increment(self, increment_by=1):
        self.number += increment_by

    def __repr__(self):
        """Return current pages count."""
        return self.number

    def current(self):
        """Return current pages count - same as __repr__ but for clarity's sake."""
        return self.number

