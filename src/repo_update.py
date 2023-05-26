#!/bin/python
import os
from datetime import datetime
from typing import Tuple
import cicd_config


class CoreQueue(object):
    def __init__(self):
        self.val_list = []
        self.id_list = []

    def clear(self):
        self.val_list.clear()
        self.id_list.clear()

    def sw_branch(self, bran_name: str):
        cmd = 'git symbolic-ref --short HEAD'
        # check if already in this branch
        cur_branch = cicd_config.exec_cmd(cmd)
        if cur_branch == (bran_name + "\n"):
            return
        else:
            # switch to branch
            print("switch to branch: " + bran_name)
            cmd = 'git checkout ' + bran_name
            ret = cicd_config.exec_cmd(cmd)
            print(ret)

    # return: (state: Bool, submod_name: str, std_date: str)
    # state: if submod repo has new commit
    def check_remote_update(self, submod_name: str) -> (Tuple[bool, str, str]):
        os.chdir(cicd_config.SUBMIT_DIR + submod_name)
        cmd = 'git rev-parse HEAD'
        local_rev = cicd_config.exec_cmd(cmd)

        self.sw_branch(cicd_config.BRANCH_NAME_DEV)
        cmd = 'git remote -v update'
        cicd_config.exec_cmd(cmd)

        cmd = 'git rev-parse origin/HEAD'
        remote_rev = cicd_config.exec_cmd(cmd)

        cmd = 'git log origin/' + cicd_config.BRANCH_NAME_DEV
        cmd += ' --pretty=format:"%s" -1'
        title_rev = cicd_config.exec_cmd(cmd)

        cmd = 'git log origin/' + cicd_config.BRANCH_NAME_DEV
        cmd += ' --pretty=format:"%ad" -1'
        date_rev = cicd_config.exec_cmd(cmd)
        print(date_rev)

        std_date = datetime.strptime(
            date_rev, cicd_config.GMT_FORMAT).strftime(cicd_config.STD_FOMRAT)

        os.chdir(cicd_config.HOME_DIR)
        print(submod_name + " local is: " + local_rev)
        print(submod_name + " remote is: " + remote_rev)
        print(submod_name + " git info is: " + title_rev + '\n')
        print(submod_name + " commit time is: " + std_date + '\n')

        if local_rev == remote_rev or title_rev != 'soc':
            return (False, submod_name, std_date)
        else:
            return (True, submod_name, std_date)

    def pull_sub(self, submod_name: str):
        os.chdir(cicd_config.SUBMIT_DIR + submod_name)
        self.sw_branch(cicd_config.BRANCH_NAME_DEV)

        cmd = 'git pull --progress -v --no-rebase "origin" '
        cmd += cicd_config.BRANCH_NAME_DEV
        ret = cicd_config.exec_cmd(cmd)
        print(ret)
        os.chdir(cicd_config.HOME_DIR)

    def check_repo(self, core_id: str):
        submod_name = 'submit/' + core_id
        ret = self.check_remote_update(submod_name)
        # restart is also right
        if core_id not in self.id_list:
            print(">>> remote repo: " + submod_name +
                  " first build! start pull...")
            self.id_list.append(core_id)
            self.pull_sub(submod_name)
            self.val_list.append(ret[1:])
        elif ret[0] is True:
            print(">>> remote repo: " + submod_name +
                  " changed! start pull...")
            self.pull_sub(submod_name)
            self.val_list.append(ret[1:])
        else:
            print(">>> remote repo: " + submod_name + " not changed")
        return ret

    def add_id(self):
        os.chdir(cicd_config.HOME_DIR)
        # check if cores have been added to the cicd database
        with open(cicd_config.ID_LIST_PATH, 'r+', encoding='utf-8') as fp:
            for v in fp:
                self.id_list.append(v.rstrip('\n'))

    def check_id(self):
        core_id = os.listdir(cicd_config.SUB_DIR)
        core_id.sort()
        for v in core_id:
            self.check_repo(v)

    def update_id(self):
        os.chdir(cicd_config.HOME_DIR)
        with open(cicd_config.ID_LIST_PATH, 'w+', encoding='utf-8') as fp:
            for v in self.id_list:
                fp.write(v + '\n')

    def update_queue(self):
        # cicd_config.git_commit(cicd_config.SUB_DIR, '[bot] update repo')
        # self.val_list = [('submit/ysyx_23050153', '2022-08-18 09:05:40'),
        #          ('submit/ysyx_23050340', '2022-08-18 09:00:38'),
        #          ('submit/ysyx_23050171', '2022-08-18 09:05:47')]
        self.val_list.sort(key=lambda v: v[1])
        with open(cicd_config.QUEUE_LIST_PATH, 'r+', encoding='utf-8') as fp:
            fp_cores = fp.readlines()
            # print(fp_cores)
            # print(self.val_list)
            # check if new-submit cores are in self.val_list
            for i, va in enumerate(fp_cores):
                for j, vb in enumerate(self.val_list):
                    if va.split()[0] == vb[0]:
                        fp_cores[i] = self.val_list[j][
                            0] + ' ' + self.val_list[j][1] + '\n'
                        self.val_list[j] = '@'

            for v in self.val_list:
                if v != '@':
                    fp_cores.append(v[0] + ' ' + v[1] + '\n')

            # print(fp_cores)
            # print(self.val_list)
            fp.seek(0)
            fp.truncate(0)
            fp.flush()
            fp.writelines(fp_cores)


core_queue = CoreQueue()


def main():
    os.system('mkdir -p ' + cicd_config.DATA_DIR)
    print('[repo update]')
    core_queue.clear()
    core_queue.add_id()
    core_queue.check_id()
    core_queue.update_id()
    core_queue.update_queue()


if __name__ == '__main__':
    main()
