from unittest import TestCase
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy as sa
from template import Template


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


class TestTemplate(TestCase):
    def setUp(self) -> None:
        self.test_template = Template(Test, TestSchema, ("username", "score"),
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

    def test_delete_item(self):
        self.test_template.delete_item("test")
        assert self.test_template.get_record("username", "test") is None

    def test_item_exists(self):
        assert self.test_template.item_exists("test") is True
        assert self.test_template.item_exists("rieuhsgihrjug") is False

    def test_get_value(self):
        assert self.test_template.get_value("test") == 500

    def test_set_value(self):
        self.test_template.set_value("test", 1)
        result = self.test_template.get_record("username", "test")
        assert result.score == 1
