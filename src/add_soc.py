#!/bin/python

import os
import cicd_config


def main():
    print('add soc')
    with open(cicd_config.SOC_LIST_DIR, 'r+') as fp:
        cores = fp.readlines()
        os.chdir(cicd_config.SUBMIT_DIR)
        for v in cores:
            tmp = v.split()
            os.system('git submodule add ' + tmp[0] + ' submit/' + tmp[1])


if __name__ == '__main__':
    main()
