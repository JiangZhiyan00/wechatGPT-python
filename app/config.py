from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini', encoding='utf-8')


def get_config(section, option):
    return config.get(section, option)
