from sqlalchemy import MetaData, Table, Column, Integer, String
from os import path


def check_for_database(database_file, engine):
    if not path.exists(database_file):
        create_default_database(database_file, engine)


def create_default_database(database_file, engine):
    meta = MetaData()
    scores = Table(
        "scores",
        meta,
        Column("id", Integer, primary_key=True),
        Column("username", String, unique=True),
        Column("score", Integer),
    )

    quotes = Table(
        "quotes",
        meta,
        Column("id", Integer, primary_key=True),
        Column("quote", String, unique=True),
    )

    commands = Table(
        "commands",
        meta,
        Column("id", Integer, primary_key=True),
        Column("command_name", String, unique=True),
        Column("message", String),
    )

    shop = Table(
        "shop",
        meta,
        Column("id", Integer, primary_key=True),
        Column("item_name", String, unique=True),
        Column("price", Integer),
    )

    emotes = Table(
        "emotes",
        meta,
        Column("id", Integer, primary_key=True),
        Column("emote_name", String, unique=True),
        Column("payout_value", Integer),
    )
    meta.create_all(engine)
