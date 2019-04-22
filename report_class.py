"""
This module defines class BrowsingReport which serves both as log and as report.
"""

import time


class BrowsingReport:
    """
    Its objects may serve as logs printed out during program execution and/or as reports printed out afterwards.
    write_report(): serves as log
    __repr__(): serves as report, is dependant from write_report()
    """

    def __init__(self):
        """Create object of BrowsingReport with attribute 'report' as empty str."""
        self.report = ''

    def write_report_info(self, line):
        self.report += line

    def write_report(self, called_function):
        """For every function passed to this method write info to report attribute and print out log.

        For each function called as attribute of this method following data will be printed into log:
        - execution starting time
        - function name
        - execution time
        Same data is written into report attribute.

        Example
        -------
            [20:24:47] determine_startpoint     	  5s
            [20:24:52] click_status_and_search  	  8s
            [20:25:00] set_strony               	  3s
        """
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
        self.report += elapsed + '\n'
        print(elapsed)

        return returned_value

    def __repr__(self):
        """Return whole object."""
        return self.report
