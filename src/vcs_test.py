#!/bin/python
from enum import Enum
import os
import cicd_config


class LogState(Enum):
    start = 0
    end = 1


class VcsTest(object):
    def __init__(self):
        self.dut = ''
        self.lint = []
        self.warn = []
        self.err = []

    def clear(self):
        self.dut = ''
        self.lint = []
        self.warn = []
        self.err = []
        self.clear_dir()

    def clear_dir(self):
        cmd = 'cd ' + cicd_config.VCS_RUN_DIR
        cmd += ' && make clean'
        cmd += ' && rm temp.fp getReg* novas* verdi* -rf'
        os.system(cmd)
        cmd = 'find ' + cicd_config.VCS_CPU_DIR + '/*'
        cmd += ' grep -v ysyx_210000.v | xargs rm -rf'
        os.system(cmd)

    def intg_soc(self):
        pass

    def comp(self):
        cmd = 'cd ' + cicd_config.VCS_RUN_DIR
        cmd += ' && make comp'
        os.system(cmd)

        log_state = [LogState.end, LogState.end, LogState.end]
        # NOTE: receive comp log
        with open(cicd_config.VCS_RUN_DIR + '/compile.log',
                  'r',
                  encoding='utf-8') as fp:
            for line in fp:
                if line[0:4] == 'Lint':
                    log_state[0] = LogState.start
                elif line[0:7] == 'Warning':
                    log_state[1] = LogState.start
                elif line[0:5] == 'Error':
                    log_state[2] = LogState.start
                elif line == '\n':
                    log_state = [LogState.end, LogState.end, LogState.end]

                if log_state[0] == LogState.start:
                    self.lint.append(line)
                elif log_state[1] == LogState.start:
                    self.warn.append(line)
                elif log_state[2] == LogState.start:
                    self.err.append(line)

    def run(self):
        pass


vcstest = VcsTest()


def main():
    print('[vcs test]')
    vcstest.clear()
    vcstest.intg_soc()
    vcstest.comp()
    vcstest.run()


if __name__ == '__main__':
    main()
