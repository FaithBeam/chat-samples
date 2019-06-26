from unittest import TestCase
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from database_connection import DatabaseConnection
import sqlalchemy as sa


engine = create_engine('sqlite://')
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class Test(Base):
    __tablename__ = "test"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, unique=True)

    def __repr__(self):
        return "<Test(username={self.username!r})>".format(self=self)


class TestSchema(ModelSchema):
    class Meta:
        model = Test
        sqla_session = session


class TestDatabaseConnection(TestCase):
    def setUp(self) -> None:
        self.db_test = DatabaseConnection(Test)
        meta = MetaData()
        test = Table(
            'test', meta,
            Column('id', Integer, primary_key=True),
            Column('username', String, unique=True)
        )
        meta.create_all(engine)
        test = Test(username="test")
        test_schema = TestSchema()
        # session.add(test)
        # session.commit()

    def tearDown(self) -> None:
        Test.__table__.drop()

    def test_get_row(self):
        print(self.db_test.get_row("username", "test"))
