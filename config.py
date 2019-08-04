import configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from databases.create_database import check_for_database

config_file = "./config/config.ini"
config = configparser.ConfigParser()
config.read(config_file)

credentials_file = "./config/credentials.ini"
credentials = configparser.ConfigParser()
credentials.read(credentials_file)

db_dialect = config["DATABASE"]["DIALECT"].strip('"')
db_destination = config["DATABASE"]["DESTINATION"].strip('"')
engine = create_engine(f"{db_dialect}{db_destination}", echo=False)
if "sqlite" in db_dialect:
    check_for_database(db_destination, engine)

session = scoped_session(sessionmaker(bind=engine))
