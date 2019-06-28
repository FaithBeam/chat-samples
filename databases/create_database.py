from sqlalchemy import MetaData, Table, Column, Integer, String
from os import path


def check_for_database(database_file, engine):
    if not path.exists(database_file):
        create_default_database(database_file, engine)


def create_default_database(database_file, engine):
    meta = MetaData()
    scores = Table(
        'scores', meta,
        Column('id', Integer, primary_key=True),
        Column('Username', String, unique=True),
        Column('Score', Integer),
    )

    quotes = Table(
        'quotes', meta,
        Column('id', Integer, primary_key=True),
        Column('Quote', String, unique=True)
    )

    commands = Table(
        'commands', meta,
        Column('id', Integer, primary_key=True),
        Column('Command Name', String, unique=True),
        Column('Message', String)
    )

    shop = Table(
        'shop', meta,
        Column('id', Integer, primary_key=True),
        Column('Item Name', String, unique=True),
        Column('Price', Integer)
    )

    emotes = Table(
        'emotes', meta,
        Column('id', Integer, primary_key=True),
        Column('Emote Name', String, unique=True),
        Column('Payout Value', Integer)
    )
    meta.create_all(engine)