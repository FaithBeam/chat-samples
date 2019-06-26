import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema
from config import engine, session

Base = declarative_base()


class Score(Base):
    __tablename__ = "scores"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, unique=True)
    score = sa.Column(sa.Integer)

    def __repr__(self):
        return "<Score(username={self.username!r}, score={self.score!r})>".format(self=self)

class ScoreSchema(ModelSchema):
    class Meta:
        model = Score
        sqla_session = session


Base.metadata.create_all(engine)