import os
import cicd_config
import tomli


def vcs_config_parse():
    pass


def dc_config_parse():
    pass


def main(sid: str):
    repo_path = cicd_config.SUB_DIR + '/' + sid
    # tmp = repo_path + '/def_config.toml'
    tmp = 'def_config.toml'
    if os.path.isfile(tmp):
        with open(tmp, 'rb') as fp:
            res = tomli.load(fp)
            print(res)

            cmd = 'git log origin/' + cicd_config.BRANCH_NAME_DEV
            cmd += ' ' + repo_path
            cmd += ' --pretty=format:"%s" -1'
            print(cmd)
            # commit_info = cicd_config.exec_cmd(cmd)
            commit_info = 'vcs'
            print(res.keys())
            if commit_info in res.keys():
                pass
            else:
                print('commit info is not found!')
    else:
        print('def_config.toml is not found!')


if __name__ == '__main__':
    main('')
