#!/usr/bin/env python

## $Id$

# This tests whether the most basic mechanisms are working Also whether stderr
# output is reported correctly Also tests if water levels are working
# correctly

from testbase import *

class UserUC(User):
    def __init__(self):
        User.__init__(self)
        self.project_prefs = "<project_specific>\nfoobar\n</project_specific>"
        self.global_prefs  = """<venue name=\"home\">
<work_buf_min_days>0</work_buf_min_days>
<work_buf_max_days>2</work_buf_max_days>
<disk_interval>1</disk_interval>
<run_on_batteries/>
<max_bytes_sec_down>400000</max_bytes_sec_down>
</venue>"""

class WorkUC(Work):
    def __init__(self, redundancy, **kwargs):
        Work.__init__(self, redundancy=redundancy)
        self.wu_template = "uc_wu"
        self.result_template = "uc_result"
        self.input_files = ['input']
        self.__dict__.update(kwargs)

class ResultUC(Result):
    def __init__(self):
        self.stderr_out   = MATCH_REGEXPS([
            "<stderr_txt>\n" +
            "APP: upper_case: starting, argc \\d+\n" +
            "APP: upper_case: argv[[]0[]] is upper_case",
            "APP: upper_case ending, wrote \\d+ chars"])

class ResultComputeErrorUC(ResultComputeError):
    def __init__(self):
        self.stderr_out   = MATCH_REGEXPS([ """<stderr_txt>
APP: upper_case: starting, argc \\d+"""])

## TODO: check that uc_wu_%d_0 matches uc_correct_output BEFORE deleted by
## file deleter!

class ProjectUC(TestProject):
    def __init__(self,
                 num_wu=None, redundancy=None,
                 expect_success=True,
                 works=None, users=None, hosts=None,
                 short_name=None, long_name=None,
                 resource_share=1):
        (num_wu, redundancy) = get_redundancy_args(num_wu, redundancy)
        TestProject.__init__(self,
                             appname = 'upper_case',
                             num_wu=num_wu, redundancy=redundancy,
                             expected_result = (expect_success and ResultUC() or ResultComputeErrorUC()),
                             works = works or [WorkUC(redundancy=redundancy)],
                             users = users or [UserUC()],
                             hosts = hosts,
                             short_name=short_name, long_name=long_name,
                             resource_share=resource_share
                             )

if __name__ == '__main__':
    test_msg("standard upper_case application");
    ProjectUC()
    run_check_all()
