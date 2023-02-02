#!/bin/python

import os
import re
import cicd_config

# ysyx4: (url, ysyx_040xxx)
# >=ysyx5: (url, ysyx_22050xxx)
# pattern: ysyx_([0-9]{6})
# cores: [(bran, url, id)]
cores = []
id_prfx = ['19', '19', '20', '21', '22', '22']
short_id = re.compile('ysyx_([0-9]{2})[0-9]{4}')
long_id = re.compile('ysyx_([0-9]{2})([0-9]{2})[0-9]{4}')


class CoreInfo(object):
    def __init__(self, bran, url, sid):
        self.bran = bran
        self.url = url
        self.sid = sid


def fillData(id_list, term, is_long):
    if is_long:
        bran = id_list[2].lstrip('0')
        if int(bran) <= 4:
            cores.append(CoreInfo(bran, term[0], term[1][:5] + term[1][7:]))
        else:
            cores.append(CoreInfo(bran, term[0], term[1]))
    else:
        bran = id_list[1].lstrip('0')
        if int(bran) <= 4:
            cores.append(CoreInfo(bran, term[0], term[1]))
        else:
            cores.append(
                CoreInfo(bran, term[0],
                         term[1][:5] + id_prfx[int(bran)] + term[1][5:]))


def main():
    print('[add soc]')
    with open('../data/soc_list', 'r+', encoding='utf-8') as fp:
        for v in fp.readlines():
            tmp = v.split()
            long_res = long_id.split(tmp[1])
            short_res = short_id.split(tmp[1])

            if len(long_res) == 4 and long_res[3] == '':
                fillData(long_res, tmp, True)

            elif len(short_res) == 3 and short_res[2] == '':
                fillData(short_res, tmp, False)

            else:
                print('ID: error format!')

    os.chdir(cicd_config.SUBMIT_DIR)
    for v in cores:
        print('git checkout ysyx' + v.bran)
        # os.system('git checkout ysyx' + v.bran)
        print('git submodule add ' + v.url + ' submit/' + v.sid)
        # os.system('git submodule add ' + v.url + ' submit/' + v.sid)


if __name__ == '__main__':
    main()
