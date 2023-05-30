#!/bin/python

import cicd_config
import config_parse


def main():
    # extract one file from queue_list
    with open(cicd_config.QUEUE_LIST_PATH, 'r+', encoding='utf-8') as fp:
        cores = fp.readlines()
        if cores != []:
            res = cores[0].split()
            # print(res)
            config_parse.main(res[0])
        else:
            print('this is not core in queue')


if __name__ == '__main__':
    main()
