from config import engine
from sqlalchemy import MetaData, Table, Column, Integer, String


meta = MetaData()
scores = Table(
    'scores', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True),
    Column('score', Integer),
)
meta.create_all(engine)