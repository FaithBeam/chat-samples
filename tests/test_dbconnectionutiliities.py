from unittest import TestCase
from unittest.mock import patch
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
with patch('databases.create_database.check_for_database') as mock_cfd:
    from db_connection_utilities import DbConnectionUtilities
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


class TestDbConnectionUtilities(TestCase):
    def setUp(self) -> None:
        self.test_template = DbConnectionUtilities(Test, TestSchema, ("username", "score"),
                                                   session)
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

    def test_add_item(self):
        self.test_template.add_item("test2", 50)
        assert self.test_template.get_record("username", "test2").username ==\
               "test2"

    def test_add_to_value(self):
        self.test_template.add_to_value("test", "200")
        assert self.test_template.get_value("test") == 700

    def test_delete_item(self):
        self.test_template.delete_item("test")
        assert self.test_template.get_record("username", "test") is None

    def test_item_exists(self):
        assert self.test_template.item_exists("test") is True
        assert self.test_template.item_exists("rieuhsgihrjug") is False

    def test_get_items_descending(self):
        session.add(Test(username="test2", score=100))
        session.add(Test(username="test3", score=200))
        session.add(Test(username="test4", score=300))
        assert self.test_template.get_items_descending("score") == "test: 500, test4: 300, test3: 200"

    def test_get_all_data(self):
        session.add(Test(username="test2", score=100))
        session.add(Test(username="test3", score=200))
        session.add(Test(username="test4", score=300))
        assert self.test_template.get_all_data() == {'test': 500, 'test2': 100, 'test3': 200, 'test4': 300}

    def test_get_bottom(self):
        session.add(Test(username="test2", score=100))
        session.add(Test(username="test3", score=200))
        session.add(Test(username="test4", score=300))
        assert self.test_template.get_bottom("score") == "test2: 100, test3: 200, test4: 300"

    def test_get_top(self):
        session.add(Test(username="test2", score=100))
        session.add(Test(username="test3", score=200))
        session.add(Test(username="test4", score=300))
        assert self.test_template.get_items_descending(
            "score") == "test: 500, test4: 300, test3: 200"

    def test_get_items(self):
        session.add(Test(username="test2", score=100))
        assert self.test_template.get_items() == 'test: 500, test2: 100'

    def test_get_value(self):
        assert self.test_template.get_value("test") == 500

    def test_set_value(self):
        self.test_template.set_value("test", 1)
        result = self.test_template.get_record("username", "test")
        assert result.score == 1
