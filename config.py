import configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from databases.create_database import check_for_database

home = str(Path.home())
config_file = "./config/config.ini"
config = configparser.ConfigParser()
config.read(config_file)

credentials_file = "./config/credentials.ini"
credentials = configparser.ConfigParser()
credentials.read(credentials_file)

database_file = ".\\databases\\user data.db"
engine = create_engine(f"sqlite:///{database_file}", echo = True)
check_for_database(database_file, engine)

session = scoped_session(sessionmaker(bind=engine))