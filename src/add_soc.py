#!/bin/python

import os
import cicd_config


# core format: (url, id)
def main():
    print('[ysyx_cicd] Add SoC')
    with open(cicd_config.SOC_LIST_PATH, 'r+', encoding='utf-8') as fp:
        cores = fp.readlines()
        os.chdir(cicd_config.SUBMIT_DIR)
        for v in cores:
            tmp = v.split()
            stu_url = tmp[0], stu_id = tmp[1]
            os.system('git submodule add ' + stu_url + ' submit/' + stu_id)


if __name__ == '__main__':
    main()
