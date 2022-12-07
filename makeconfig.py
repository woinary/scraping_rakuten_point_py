from configparser import ConfigParser

config = ConfigParser()
section = 'RAKUTEN'

config.add_section(section)
config.set(section, 'userid', 'ユーザID')
config.set(section, 'password', 'パスワード')

with open('.config', 'w') as file:
    config.write(file)