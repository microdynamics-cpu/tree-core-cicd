#!/bin/python

import os
import re
from typing import List
import cicd_config
from data_type import CoreInfo

# cores: [(bran, url, id)]
cores = []


# 1. pattern: ysyx_([0-9]{6})
# 2. in id list
def checkValid(val: str) -> str:
    if re.match('ysyx_[0-9]{8}', val) is not None:
        return val
    else:
        return ''


def fillData(term: List[str]):
    cores.append(CoreInfo(cicd_config.CUR_BRAN, term[0], term[1]))


def handleIDErr(val: str):
    # need to write to the submit info
    print('ID: error format, the err val: ' + val)


def main():
    print('[add soc]')
    with open(cicd_config.SOC_LIST_PATH, 'r+', encoding='utf-8') as fp:
        for v in fp.readlines():
            tmp = v.split()
            # print(tmp[1])
            if checkValid(tmp[1]) != '':
                fillData(tmp)
            else:
                handleIDErr(tmp)

    os.chdir(cicd_config.SUBMIT_DIR)
    for v in cores:
        print('git checkout ' + v.bran)
        # os.system('git checkout ' + v.bran)
        print('git submodule add ' + v.url + ' submit/' + v.sid)
        # os.system('git submodule add ' + v.url + ' submit/' + v.sid)


if __name__ == '__main__':
    main()
