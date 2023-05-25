import tomli

with open('def_config.toml', 'rb') as f:
    res = tomli.load(f)

print(res)