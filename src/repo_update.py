#!/bin/python

import os
from datetime import datetime
import cicd_config

queue = []
core_list = []

def exec_cmd(cmd):
    try:
        ret = os.popen(cmd).read()
    except:
        print("Error occured when exec_cmd")

    return ret


def sw_branch(bran_name):
    cmd = 'git symbolic-ref --short HEAD'
    # check if already in this branch
    cur_bran = exec_cmd(cmd)
    if cur_bran == (bran_name + "\n"):
        return
    else:
        # switch to branch
        print("switch to branch: " + bran_name)
        cmd = 'git checkout ' + bran_name
        ret = exec_cmd(cmd)
        print(ret)


def is_remote_update(sm_name):
    os.chdir(cicd_config.SUBMIT_DIR + sm_name)
    cmd = 'git rev-parse HEAD'
    local_rev = exec_cmd(cmd)

    sw_branch(cicd_config.BRANCH_NAME_DEV)
    cmd = 'git remote -v update'
    ret = exec_cmd(cmd)

    cmd = 'git rev-parse origin/HEAD'
    remote_rev = exec_cmd(cmd)

    cmd = 'git log origin/' + cicd_config.BRANCH_NAME_DEV + ' --pretty=format:"%s" -1'
    title_rev = exec_cmd(cmd)

    cmd = 'git log origin/' + cicd_config.BRANCH_NAME_DEV + ' --pretty=format:"%ad" -1'
    date_rev = exec_cmd(cmd)
    print(date_rev)
    std_date = datetime.strptime(date_rev,
                                 cicd_config.GMT_FORMAT).strftime(cicd_config.STD_FOMRAT)
    os.chdir(cicd_config.HOME_DIR)
    print(sm_name + " local is: " + local_rev)
    print(sm_name + " remote is: " + remote_rev)
    print(sm_name + " git info is: " + title_rev + '\n')
    print(sm_name + " commit time is: " + std_date + '\n')

    if local_rev == remote_rev or title_rev != 'dc & vcs':
        return (False, sm_name, std_date)
    else:
        return (True, sm_name, std_date)


def pull_sub(sm_name):
    os.chdir(cicd_config.SUBMIT_DIR + sm_name)
    sw_branch(cicd_config.BRANCH_NAME_DEV)

    cmd = 'git pull --progress -v --no-rebase "origin" ' + cicd_config.BRANCH_NAME_DEV
    ret = exec_cmd(cmd)
    print(ret)
    os.chdir(cicd_config.HOME_DIR)


def check_sub(sm_name):
    ret = is_remote_update(sm_name)
    if not (ret[1].split('/')[1] in core_list): # restart is also right
        print(">>> remote submodule: " + sm_name + " first build! start pull...")
        core_list.append(ret[1].split('/')[1])
        pull_sub(sm_name)
        queue.append(ret[1:])
    elif ret[0] == True:
        print(">>> remote submodule: " + sm_name + " changed! start pull...")
        pull_sub(sm_name)
        queue.append(ret[1:])
    else:
        print(">>> remote submodule: " + sm_name + " Not changed...")
    return ret

def main():
    os.system('mkdir -p data')
    # print(cicd_config.HOME_DIR)
    # print(cicd_config.SUBMIT_DIR)
    print('[ysyx_submit] Auto Git Submodule Update... \n')
    global core_list
    core_list.clear()
    os.chdir(cicd_config.HOME_DIR)
    with open('./data/core_list', 'r+') as f:
        for line in f:
            core_list.append(line.rstrip('\n'))

    cores = os.listdir(cicd_config.SUB_DIR)
    cores.sort()
    global queue
    queue.clear()
    for i in range(len(cores)):
        check_sub('submit/' + cores[i])

    os.chdir(cicd_config.HOME_DIR)
    with open('./data/core_list', 'w+') as f:
        for v in core_list:
            f.write(v + '\n')

    # cicd_config.git_commit(cicd_config.SUB_DIR, '[bot] update submodule')
    # queue = [('submit/ysyx_210153', '2022-08-18 09:05:40'),
    #          ('submit/ysyx_210340', '2022-08-18 09:00:38'),
    #          ('submit/ysyx_210171', '2022-08-18 09:05:47')]
    queue.sort(key=lambda v: v[1])

    fp = open('data/queue_list', 'r+')
    fp_cores = fp.readlines()
    # print(fp_cores)
    # print(queue)
    # check if new-submit cores are in queue
    for i in range(len(fp_cores)):
        for j in range(len(queue)):
            if fp_cores[i].split()[0] == queue[j][0]:
                fp_cores[i] = queue[j][0] + ' ' + queue[j][1] + '\n'
                queue[j] = '@'

    for v in queue:
        if v != '@':
            fp_cores.append(v[0] + ' ' + v[1] + '\n')

    # print(fp_cores)
    # print(queue)
    fp.seek(0)
    fp.truncate(0)
    fp.flush()
    fp.writelines(fp_cores)
    fp.close()


if __name__ == '__main__':
    main()
