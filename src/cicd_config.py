#!/bin/python
import os

BRANCH_NAME_DEV = 'master'

GMT_FORMAT = '%a %b %d %H:%M:%S %Y %z'
STD_FOMRAT = '%Y-%m-%d %H:%M:%S'

CUR_BRAN = '202302'
HOME_DIR = os.getcwd() + '/'
DATA_DIR = HOME_DIR + '../data/' + CUR_BRAN
SOC_LIST_PATH = DATA_DIR + '/soc_list'
CORE_LIST_PATH = DATA_DIR + '/core_list'
QUEUE_LIST_PATH = DATA_DIR + '/queue_list'

DC_HOME_DIR = HOME_DIR + '../lib/dc/bes_data/syn/scr'
DC_LOG_DIR = DC_HOME_DIR + '../log'
DC_RPT_DIR = DC_HOME_DIR + '../rpt'
# need to modify the SUBMIT_DIR path for the CICD repo
SUBMIT_DIR = '../tests/intg/'
SUB_DIR = SUBMIT_DIR + 'submit/'
RPT_DIR = SUBMIT_DIR + 'report/'


def git_commit(path, info, push=False):
    os.chdir(SUBMIT_DIR)
    os.system('git add ' + path)
    os.system('git commit -m "' + info + '"')
    if push:
        os.system('git push')
    os.chdir(HOME_DIR)
