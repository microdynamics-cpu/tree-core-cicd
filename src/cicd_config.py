#!/bin/python
import os

BRANCH_NAME_DEV = 'master'

GMT_FORMAT = '%a %b %d %H:%M:%S %Y %z'
STD_FOMRAT = '%Y-%m-%d %H:%M:%S'

HOME_DIR = os.getcwd() + '/'
SOC_LIST_DIR = HOME_DIR + '../data/soc_list'

SUBMIT_DIR = HOME_DIR + '../ysyx_submit/'
SUB_DIR = SUBMIT_DIR + 'submit/'
RPT_DIR = SUBMIT_DIR + 'report/'


def git_commit(path, info, push=False):
    os.chdir(SUBMIT_DIR)
    os.system('git add ' + path)
    os.system('git commit -m "' + info + '"')
    if push:
        os.system('git push')
    os.chdir(HOME_DIR)
