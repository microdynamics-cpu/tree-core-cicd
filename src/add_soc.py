#!/bin/python

import os
import re
from typing import List
import cicd_config
from data_type import CoreInfo


class Cores(object):
    def __init__(self):
        self.cores = []

    # 1. pattern: ysyx_([0-9]{6})
    # 2. in id list
    def check_valid(self, val: str) -> str:
        if re.match('ysyx_[0-9]{8}', val) is not None:
            return val
        else:
            return ''

    def fill_data(self, term: List[str]):
        self.cores.append(CoreInfo(cicd_config.CUR_BRAN, term[0], term[1]))

    def handle_err(self, val: str):
        # NOTE: need to write to the submit info
        print('ID: error format, the err val: ' + val)

    def add(self):
        with open(cicd_config.SOC_LIST_PATH, 'r+', encoding='utf-8') as fp:
            for v in fp.readlines():
                tmp = v.split()
                # print(tmp[1])
                if self.check_valid(tmp[1]) != '':
                    self.fill_data(tmp)
                else:
                    self.handle_err(tmp)

    def update(self):
        os.chdir(cicd_config.SUBMIT_DIR)
        for v in self.cores:
            print('git checkout ' + v.bran)
            # os.system('git checkout ' + v.bran)
            print('git submodule add ' + v.url + ' submit/' + v.sid)
            # os.system('git submodule add ' + v.url + ' submit/' + v.sid)


cores = Cores()


def main():
    print('[add soc]')
    cores.add()
    cores.update()


if __name__ == '__main__':
    main()
