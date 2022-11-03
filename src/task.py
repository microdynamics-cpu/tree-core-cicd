#!/bin/python

import schedule
import time
import add_soc
import repo_update
import soc_test


def main_task():
    add_soc.main()
    repo_update.main()
    soc_test.main()


schedule.every(3).minutes.do(main_task)

while True:
    schedule.run_pending()
    time.sleep(1)