import configparser
from pathlib import Path


home = str(Path.home())
config_file = "./config/config.ini"
config = configparser.ConfigParser()
config.read(config_file)

credentials_file = "./config/config.ini"
credentials = configparser.ConfigParser()
credentials.read(credentials_file)
