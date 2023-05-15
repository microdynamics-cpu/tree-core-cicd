#!/bin/python
import os
from datetime import datetime
from typing import Tuple
import cicd_config

queue = []
core_list = []


def exec_cmd(cmd: str) -> str:
    try:
        ret = os.popen(cmd).read()
    except Exception as e:
        print("Error '{0}' occured when exec_cmd".format(e))
        ret = ''
    return ret


def sw_branch(branch_name: str):
    cmd = 'git symbolic-ref --short HEAD'
    # check if already in this branch
    cur_branch = exec_cmd(cmd)
    if cur_branch == (branch_name + "\n"):
        return
    else:
        # switch to branch
        print("switch to branch: " + branch_name)
        cmd = 'git checkout ' + branch_name
        ret = exec_cmd(cmd)
        print(ret)


# return: (state: Bool, submod_name: str, std_date: str)
# state: if submod repo has new commit
def check_remote_update(submod_name: str) -> (Tuple[bool, str, str]):
    os.chdir(cicd_config.SUBMIT_DIR + submod_name)
    cmd = 'git rev-parse HEAD'
    local_rev = exec_cmd(cmd)

    sw_branch(cicd_config.BRANCH_NAME_DEV)
    cmd = 'git remote -v update'
    exec_cmd(cmd)

    cmd = 'git rev-parse origin/HEAD'
    remote_rev = exec_cmd(cmd)

    cmd = 'git log origin/' + cicd_config.BRANCH_NAME_DEV
    cmd += ' --pretty=format:"%s" -1'
    title_rev = exec_cmd(cmd)

    cmd = 'git log origin/' + cicd_config.BRANCH_NAME_DEV
    cmd += ' --pretty=format:"%ad" -1'
    date_rev = exec_cmd(cmd)
    print(date_rev)

    std_date = datetime.strptime(date_rev, cicd_config.GMT_FORMAT).strftime(
        cicd_config.STD_FOMRAT)

    os.chdir(cicd_config.HOME_DIR)
    print(submod_name + " local is: " + local_rev)
    print(submod_name + " remote is: " + remote_rev)
    print(submod_name + " git info is: " + title_rev + '\n')
    print(submod_name + " commit time is: " + std_date + '\n')

    if local_rev == remote_rev or title_rev != 'dc & vcs':
        return (False, submod_name, std_date)
    else:
        return (True, submod_name, std_date)


def pull_sub(submod_name: str):
    os.chdir(cicd_config.SUBMIT_DIR + submod_name)
    sw_branch(cicd_config.BRANCH_NAME_DEV)

    cmd = 'git pull --progress -v --no-rebase "origin" '
    cmd += cicd_config.BRANCH_NAME_DEV
    ret = exec_cmd(cmd)
    print(ret)
    os.chdir(cicd_config.HOME_DIR)


def check_sub(core_name: str):
    submod_name = 'submit/' + core_name
    ret = check_remote_update(submod_name)
    # restart is also right
    if core_name not in core_list:
        print(">>> remote submodule: " + submod_name +
              " first build! start pull...")
        core_list.append(core_name)
        pull_sub(submod_name)
        queue.append(ret[1:])
    elif ret[0] is True:
        print(">>> remote submodule: " + submod_name +
              " changed! start pull...")
        pull_sub(submod_name)
        queue.append(ret[1:])
    else:
        print(">>> remote submodule: " + submod_name + " Not changed...")
    return ret


def main():
    os.system('mkdir -p ' + cicd_config.DATA_DIR)
    print('[ysyx_cicd] Auto Git Submodule Update... \n')

    global core_list
    core_list.clear()

    os.chdir(cicd_config.HOME_DIR)
    with open(cicd_config.CORE_LIST_PATH, 'r+', encoding='utf-8') as fp:
        for line in fp:
            core_list.append(line.rstrip('\n'))

    cores = os.listdir(cicd_config.SUB_DIR)
    cores.sort()

    global queue
    queue.clear()

    for v in cores:
        check_sub(v)

    os.chdir(cicd_config.HOME_DIR)
    with open(cicd_config.CORE_LIST_PATH, 'w+', encoding='utf-8') as fp:
        for v in core_list:
            fp.write(v + '\n')

    # cicd_config.git_commit(cicd_config.SUB_DIR, '[bot] update submodule')
    # queue = [('submit/ysyx_210153', '2022-08-18 09:05:40'),
    #          ('submit/ysyx_210340', '2022-08-18 09:00:38'),
    #          ('submit/ysyx_210171', '2022-08-18 09:05:47')]
    queue.sort(key=lambda v: v[1])

    with open(cicd_config.QUEUE_LIST_PATH, 'r+', encoding='utf-8') as fp:
        fp_cores = fp.readlines()
        # print(fp_cores)
        # print(queue)
        # check if new-submit cores are in queue
        for i, va in enumerate(fp_cores):
            for j, vb in enumerate(queue):
                if va.split()[0] == vb[0]:
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


if __name__ == '__main__':
    main()
