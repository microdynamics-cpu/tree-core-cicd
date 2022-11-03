#!/bin/python

import os
import config


# (url, ysyx_040xxx)
def main():
    print('add soc')
    fp = open('data/soc_list', 'r+')
    cores = fp.readlines()
    os.chdir(config.SUBMIT_DIR)
    for v in cores:
        tmp = v.split()
        # print('git submoudle add ' + tmp[0] + ' submit/' + tmp[1])
        os.system('git submodule add ' + tmp[0] + ' submit/' + tmp[1])
    fp.close()


if __name__ == '__main__':
    main()