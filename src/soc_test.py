#!/bin/python

import os
import cicd_config

rpt_home = ''
dut_core = ''
lint = []
warning = []
error = []
run_warning = []
flag = [0, 0, 0]


def comp_test():
    global lint
    lint.clear()
    global warning
    warning.clear()
    global error
    error.clear()
    global run_warning
    run_warning.clear()
    global flag
    flag = [0, 0, 0]

    os.system("cd ./vcs/run && make comp")
    comp_fp = open("./vcs/run/compile.log", 'r')
    lint.clear()
    warning.clear()
    error.clear()
    for line in comp_fp:
        if flag[0] == 1:
            if 'vga' in line:
                flag[0] = 0
                lint.pop()
                continue
            lint.append(line)
            if line == '\n':
                lint.append(line)
                flag[0] = 0
        if flag[1] == 1:
            warning.append(line)
            if line == '\n':
                warning.append(line)
                flag[1] = 0
        if flag[2] == 1:
            error.append(line)
            if line == '\n':
                error.append(line)
                flag[2] = 0
        elif line[0:4] == 'Lint':
            flag[0] = 1
            lint.append(line)
        elif line[0:7] == 'Warning':
            flag[1] = 1
            warning.append(line)
        elif line[0:5] == 'Error':
            flag[2] = 1
            error.append(line)
    comp_fp.close()

    fp = open(rpt_home + '/vcs_report', 'a+')
    fp.writelines('\ncore:  ' + dut_core + '\n')
    fp.writelines(
        '\n#####################\n#vcs compile log\n#####################\n')
    fp.writelines(error + warning + lint)
    if error == [] and warning == [] and lint == []:
        fp.writelines("\n\n\nall clear!!\n\n\n")
    fp.close()

    return error == [] and lint == []


def system_test():

    hello_test_flash = 0
    hello_test_ram = 0
    hello_test_sdram = 0
    mem_test_flash = 0
    mem_test_ram = 0
    mem_test_sdram = 0
    rtthread_test_flash = 0
    rtthread_test_ram = 0
    rtthread_test_sdram = 0
    err_cnt = 0

    fp = open(rpt_home + '/vcs_report', 'a+')
    if error == []:
        fp.writelines(
            '\n#####################\n#vcs system test\n#####################\n'
        )
        os.system(
            "cd ./vcs/run && ln -sf program/hello.flash mem_Q128_bottom.vmf && make run test=hello_test_flash"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if flag[1] == 1:
                run_warning.append(line)
                if line == '\n':
                    run_warning.append(line)
                    flag[1] = 0
            if line[0:7] == 'Warning':
                flag[1] = 1
                run_warning.append(line)
            if "Hello World!" in line:
                hello_test_flash = 1

        os.system(
            "cd ./vcs/run && ln -sf program/jump.ram mem_Q128_bottom.vmf && ln -sf program/hello.ram init_mem.bin.txt && make run test=hello_test_ram"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if flag[1] == 1:
                run_warning.append(line)
                if line == '\n':
                    run_warning.append(line)
                    flag[1] = 0
            if line[0:7] == 'Warning':
                flag[1] = 1
                run_warning.append(line)
            if "Hello World!" in line:
                hello_test_ram = 1

        os.system(
            "cd ./vcs/run && ln -sf program/jump.sdram mem_Q128_bottom.vmf && ln -sf program/hello.sdram init_sdram.bin.txt && make run test=hello_test_sdram"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if flag[1] == 1:
                run_warning.append(line)
                if line == '\n':
                    run_warning.append(line)
                    flag[1] = 0
            if line[0:7] == 'Warning':
                flag[1] = 1
                run_warning.append(line)
            if "Hello World!" in line:
                hello_test_sdram = 1

        os.system(
            "cd ./vcs/run && ln -sf program/memtest.flash mem_Q128_bottom.vmf && make run test=mem_test_flash"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if "ALL TESTS PASSED!!" in line:
                mem_test_flash = 1

        os.system(
            "cd ./vcs/run && ln -sf program/jump.ram mem_Q128_bottom.vmf && ln -sf program/memtest.ram init_mem.bin.txt && make run test=mem_test_ram"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if "ALL TESTS PASSED!!" in line:
                mem_test_ram = 1

        os.system(
            "cd ./vcs/run && ln -sf program/jump.sdram mem_Q128_bottom.vmf && ln -sf program/memtest.sdram init_sdram.bin.txt && make run test=mem_test_sdram"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if "ALL TESTS PASSED!!" in line:
                mem_test_sdram = 1

        os.system(
            "cd ./vcs/run && ln -sf program/rtthread.flash mem_Q128_bottom.vmf && make run test=rtthread_test_flash"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if "Hello RISC-V!" in line:
                rtthread_test_flash = 1

        os.system(
            "cd ./vcs/run && ln -sf program/jump.ram mem_Q128_bottom.vmf && ln -sf program/rtthread.ram init_mem.bin.txt && make run test=rtthread_test_ram"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if "Hello RISC-V!" in line:
                rtthread_test_ram = 1

        os.system(
            "cd ./vcs/run && ln -sf program/jump.sdram mem_Q128_bottom.vmf && ln -sf program/rtthread.sdram init_sdram.bin.txt && make run test=rtthread_test_sdram"
        )
        for line in open('./vcs/run/run.log', 'r', encoding='ISO-8859-1'):
            if "Hello RISC-V!" in line:
                rtthread_test_sdram = 1

        fp.writelines(run_warning)
        if hello_test_flash == 1:
            fp.writelines('Hello test in flash pass!!\n')
        else:
            fp.writelines('!!!!Hello test in flash fail!!!!\n')
            err_cnt += 1

        if hello_test_ram == 1:
            fp.writelines('Hello test in mem pass!!\n')
        else:
            fp.writelines('!!!!Hello test in mem fail!!!!\n')
            err_cnt += 1

        if hello_test_sdram == 1:
            fp.writelines('Hello test in sdram pass!!\n')
        else:
            fp.writelines('!!!!Hello test in sdram fail!!!!\n')
            err_cnt += 1

        if mem_test_flash == 1:
            fp.writelines('Mem test in flash pass!!\n')
        else:
            fp.writelines('!!!!Mem test in flash fail!!!!\n')
            err_cnt += 1

        if mem_test_ram == 1:
            fp.writelines('Mem test in mem pass!!\n')
        else:
            fp.writelines('!!!!Mem test in mem fail!!!!\n')
            err_cnt += 1

        if mem_test_sdram == 1:
            fp.writelines('Mem test in sdram pass!!\n')
        else:
            fp.writelines('!!!!Mem test in sdram fail!!!!\n')
            err_cnt += 1

        if rtthread_test_flash == 1:
            fp.writelines('rtthread test in flash pass!!\n')
        else:
            fp.writelines('!!!!rtthread test in flash fail!!!!\n\n\n')
            err_cnt += 1

        if rtthread_test_ram == 1:
            fp.writelines('rtthread test in mem pass!!\n')
        else:
            fp.writelines('!!!!rtthread test in mem fail!!!!\n\n\n')
            err_cnt += 1

        if rtthread_test_sdram == 1:
            fp.writelines('rtthread test in sdram  pass!!\n')
        else:
            fp.writelines('!!!!rtthread test in sdram fail!!!!\n\n\n')
            err_cnt += 1

        # if hello_test_flash == 0 or hello_test_ram == 0 or hello_test_sdram == 0 or mem_test_flash == 0 or mem_test_ram == 0 or mem_test_sdram == 0 or rtthread_test_flash == 0 or rtthread_test_ram == 0 or rtthread_test_sdram == 0:
        #     temp = open("./vcs/run/temp.fp", 'w')
        #     temp.writelines(
        #         "../tb/asic_system.v\n../top/asic_top.v\n../top/soc_top.v\n../cpu/"
        #         + dut_core)
        #     temp.close()
        #     os.system(
        #         "cd ./vcs/run && ln -sf program/hello.flash mem_Q128_bottom.vmf && make run test=dump_fsdb && getRegValues_batch.pl -fp ./temp.fp  -fsdb asic_top.fsdb  -val_time 300000 -time_unit ns -o getRegValues.log "
        #     )
        #     regvalue = open("./vcs/run/getRegValues.log", 'r')
        #     fp.writelines(
        #         "程序未跑通，可能是由于某些寄存器控制信号未初始化，或是某些逻辑错误,请自行检查修正后再次提交测试\n\n")
        #     promt = 0
        #     for line in regvalue:
        #         if dut_core in line:
        #             if 'x' in line[line.rfind('='):]:
        #                 if promt == 0:
        #                     fp.writelines('以下为未复位的寄存器:\n\n')
        #                     promt = 1
        #                 fp.writelines(line.split('=')[0] + '\n')

    fp.close()

    return err_cnt == 0


def create_rpt_dir():
    is_have = False
    fp = open('data/queue_list', 'r+')
    cores = fp.readlines()
    if cores != []:
        rec = cores[0].split()
        global dut_core
        dut_core = rec[0].split('/')[1]

        # record queue state
        os.system('mkdir -p ' + cicd_config.RPT_DIR + dut_core)
        os.system('echo state: under test > ' + cicd_config.RPT_DIR +
                  dut_core + '/state')

        # remove record from queue
        fp.seek(0)
        fp.truncate(0)
        fp.flush()
        fp.writelines(cores[1:])
        is_have = True

        # update other cores state
        fp.seek(0)
        cores = fp.readlines()
        cnt = 1
        for v in cores:
            v_path = cicd_config.RPT_DIR + v.split()[0].split('/')[1]
            os.system('mkdir -p ' + v_path)
            os.system('echo state: wait ' + str(cnt) + ' cores > ' + v_path +
                      '/state')
            cnt += 1

        cicd_config.git_commit(cicd_config.RPT_DIR,
                               '[bot] update soc state file', True)

        # soc integration
        global rpt_home
        rpt_home = cicd_config.RPT_DIR + dut_core + '/' + rec[1] + '...' + rec[
            2]
        os.system('mkdir -p ' + rpt_home)
        soc_intg(rec)
    else:
        print('this is not core in queue')

    fp.close()
    return is_have


def soc_intg(rec):
    core_path = cicd_config.SUBMIT_DIR + rec[0] + '/' + rec[0].split('/')[1]
    v_format = core_path + '.v'
    sv_format = core_path + '.sv'
    if os.path.isfile(v_format):
        os.system('cp ' + v_format + ' ./vcs/cpu')
    elif os.path.isfile(sv_format):
        os.system('cp ' + sv_format + ' ' + v_format)
        os.system('mv ' + v_format + ' ./vcs/cpu')
    else:
        print('no core file!')

    # print('cp ' + cicd_config.SUBMIT_DIR  + rec[0] + '/' + rec[0] + '.v')
    os.chdir('./vcs/script')
    os.system('python autowire.py')
    os.chdir('../../')


def clean_vcs_env():
    os.system(
        'cd ./vcs/run && make clean && rm temp.fp getReg* novas* verdi* -rf')
    os.system('find ./vcs/cpu/* | grep -v ysyx_210000.v | xargs rm -rf')


def clean_dc_env():
    os.chdir(cicd_config.HOME_DIR + 'dc/bes_data/syn/')
    # os.system('rm -rf log/*.log')
    # os.system('rm -rf out/*.txt')
    os.chdir(cicd_config.HOME_DIR)


def run_vcs():
    is_comp_right = comp_test()
    is_run_right = False
    if (is_comp_right):
        is_run_right = system_test()
    return is_comp_right and is_run_right


def run_main():
    clean_vcs_env()  # can not move into create_rpt_dir!
    if create_rpt_dir():
        is_vcs_right = run_vcs()
        if (is_vcs_right):
            run_dc()
        cicd_config.git_commit(cicd_config.RPT_DIR, '[bot] new report!', True)


def run_dc():
    clean_dc_env()
    os.system('rm -rf ./vcs/cpu_dc/*.v')
    os.system('cp ./vcs/cpu/' + dut_core + '.v ./vcs/cpu_dc/')
    os.chdir('./vcs/script')
    os.system('./autowire_new.py')
    os.chdir(cicd_config.HOME_DIR)
    os.chdir('./dc/bes_data/syn/scr/')
    os.system('./syn_scr_update')
    os.system('cp ../out/dc_report ' + rpt_home)
    clean_dc_env()
    clean_vcs_env()  # can not move into run_vcs!
    os.chdir(cicd_config.HOME_DIR)


def main():
    print('soc test')
    run_main()


if __name__ == '__main__':
    main()
