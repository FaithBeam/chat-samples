import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema
from config import engine, session

Base = declarative_base()


class Quotes(Base):
    __tablename__ = "commands"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    quote = sa.Column(sa.String, unique=True)

    def __repr__(self):
        return "<Quotes(Quote={self.quote!r})>".format(self=self)

class QuotesSchema(ModelSchema):
    class Meta:
        model = Quotes
        sqla_session = session


class Commands(Base):
    __tablename__ = "commands"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    command_name = sa.Column(sa.String, unique=True)
    message = sa.Column(sa.String)

    def __repr__(self):
        return "<Commands(Command Name={self.command_name!r}, Message={self.message!r})>".format(self=self)

class CommandsSchema(ModelSchema):
    class Meta:
        model = Commands
        sqla_session = session


class Shop(Base):
    __tablename__ = "shop"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    item_name = sa.Column(sa.String, unique=True)
    price = sa.Column(sa.Integer)

    def __repr__(self):
        return "<Shop(Item Name={self.item_name!r}, Price={self.price!r})>".format(self=self)


class ShopSchema(ModelSchema):
    class Meta:
        model = Shop
        sqla_session = session


class Emotes(Base):
    __tablename__ = "emotes"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    emote_name = sa.Column(sa.String, unique=True)
    payout_value = sa.Column(sa.Integer)

    def __repr__(self):
        return "<Emotes(Emote Name={self.emote_name!r}, Payout Value={self.payout_value!r})>".format(self=self)

class EmoteSchema(ModelSchema):
    class Meta:
        model = Emotes
        sqla_session = session


class Score(Base):
    __tablename__ = "scores"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, unique=True)
    score = sa.Column(sa.Integer)

    def __repr__(self):
        return "<Score(Username={self.username!r}, Score={self.score!r})>".format(self=self)

class ScoreSchema(ModelSchema):
    class Meta:
        model = Score
        sqla_session = session


Base.metadata.create_all(engine)