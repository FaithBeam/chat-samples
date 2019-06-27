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
    score = sa.Column(sa.Integer)

    def __repr__(self):
        return "<Test(username={self.username!r})>".format(self=self)


class TestSchema(ModelSchema):
    class Meta:
        model = Test
        sqla_session = session


class TestDatabaseConnection(TestCase):
    def setUp(self) -> None:
        self.db_test = DatabaseConnection(Test, session)
        meta = MetaData()
        test = Table(
            'test', meta,
            Column('id', Integer, primary_key=True),
            Column('username', String, unique=True),
            Column('score', Integer)
        )
        meta.create_all(engine)
        test = Test(username="test", score=500)
        session.add(test)
        session.commit()

    def tearDown(self) -> None:
        Base.metadata.drop_all(engine)

    def test_bottom(self):
        session.add(Test(username="test2", score=100))
        session.add(Test(username="test3", score=200))
        session.add(Test(username="test4", score=300))
        rows = self.db_test.bottom("score")
        current = rows[0]
        for row in rows:
            assert current.score <= row.score

    def test_count_records(self):
        assert self.db_test.count_records() == 1

    def test_delete_record(self):
        self.db_test.delete_record("username", "test")
        record = self.db_test.get_record("username", "test")
        if record:
            self.fail()
        else:
            pass

    def test_get_all_records(self):
        rows = self.db_test.get_all_records()
        assert rows[0].username == Test(username="test", score=500).username
        assert rows[0].score == Test(username="test", score=500).score
        assert rows[0].id == 1

    def test_get_record(self):
        assert self.db_test.get_record("username", "test").username == "test"
        assert self.db_test.get_record("username", "test").score == 500

    def test_insert_record(self):
        self.db_test.insert_record(Test(username="test2", score=100))
        assert self.db_test.get_record("username", "test2").username == "test2"

    def test_top(self):
        session.add(Test(username="test2", score=100))
        session.add(Test(username="test3", score=200))
        session.add(Test(username="test4", score=300))
        rows = self.db_test.top("score")
        current = rows[0]
        for row in rows:
            assert current.score >= row.score

    def test_update_record(self):
        self.db_test.update_document("username", "test", "changed")
        assert self.db_test.get_record("username", "changed").username == \
               "changed"
