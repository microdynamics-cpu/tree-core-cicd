import tomli


def main():
    with open('def_config.toml', 'rb') as f:
        res = tomli.load(f)
        print(res)


if __name__ == '__main__':
    main()
