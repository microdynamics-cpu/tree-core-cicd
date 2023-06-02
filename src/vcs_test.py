#!/bin/python
import os


class VcsTest(object):
    def __init__(self):
        pass

    def clear(self):
        cmd = 'cd lib/vcs/run && make clean && '
        cmd += 'rm temp.fp getReg* novas* verdi* -rf'
        os.system(cmd)
        cmd = 'find lib/vcs/cpu/* | grep -v ysyx_210000.v | xargs rm -rf'
        os.system(cmd)

    def create_dir(self):
        pass


vcstest = VcsTest()


def main():
    print('[vcs test]')
    vcstest.clear()


if __name__ == '__main__':
    main()
