#!/bin/python

import os
import re
from typing import List
import cicd_config
from data_type import CoreInfo


class Cores(object):
    def __init__(self):
        self.cores = []
        self.id_list = []

    def clear(self):
        self.cores.clear()
        self.id_list.clear()

    # 1. pattern: ysyx_([0-9]{6})
    # 2. in id list
    def check_valid(self, val: str) -> str:
        if re.match('ysyx_[0-9]{8}', val) is not None:
            return val
        else:
            return ''

    def fill_data(self, term: List[str]):
        self.cores.append(CoreInfo(term[0], term[1]))

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

    # update the id list
    def update(self):
        os.chdir(cicd_config.SUBMIT_DIR)
        # os.system('git checkout ' + cicd_config.CUR_BRAN)
        print('git checkout ' + cicd_config.CUR_BRAN)
        with open(cicd_config.ID_LIST_PATH, 'r+', encoding='utf-8') as fp:
            for v in fp:
                val = v.rstrip('\n')
                # print('id: ' + val)
                # filter err and spaces
                if self.check_valid(val) != '':
                    self.id_list.append(v.rstrip('\n'))
                # print('id: ' + v.rstrip('\n'))

        self.id_list.sort()
        self.cores.sort(key=lambda v: v.sid)

        new_id = []
        for va in self.cores:
            is_find = False
            for vb in self.id_list:
                if va.sid == vb:
                    is_find = True
                    break

            if is_find is False:
                # os.system('git submodule add ' + va.url + ' submit/' + va.sid)
                print('git submodule add ' + va.url + ' submit/' + va.sid)
                new_id.append(va.sid)

        self.id_list += new_id
        self.id_list.sort()
        # print(self.id_list)
        with open(cicd_config.ID_LIST_PATH, 'w+', encoding='utf-8') as fp:
            for v in self.id_list:
                fp.write(v + '\n')


cores = Cores()


def main():
    print('[add soc]')

    cores.clear()
    cores.add()
    cores.update()


if __name__ == '__main__':
    main()
