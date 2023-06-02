#!/bin/python

import cicd_config
import config_parse
import iv_test
import ver_test
import vcs_test
# import dc_test


def main():
    # extract one file from queue_list
    with open(cicd_config.QUEUE_LIST_PATH, 'r+', encoding='utf-8') as fp:
        cores = fp.readlines()
        if cores != []:
            tmp = cores[0].split()
            # print(tmp)
            res = config_parse.main(tmp[0])
            if res[1] == 'iv':
                iv_test.main()
            elif res[1] == 'ver':
                ver_test.main()
            elif res[1] == 'vcs':
                vcs_test.main()
            elif res[1] == 'dc':
                # dc_test.main()
                pass
        else:
            print('this is not core in queue')


if __name__ == '__main__':
    main()
