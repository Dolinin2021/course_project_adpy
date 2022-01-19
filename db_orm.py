import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DSN = 'postgresql+psycopg2://ilya:12345@localhost:5432/adpy_course_project'
Base = declarative_base()

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
session = Session()

ban_list = []
favorite_list = []


class BanList(Base):
    __tablename__ = 'ban_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


class FavoriteList(Base):
    __tablename__ = 'favorite_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


query_value_ban_list = session.query(BanList).all()
for row in query_value_ban_list:
    ban_list.append(row.id)

query_value_favorite_list = session.query(FavoriteList).all()
for row in query_value_favorite_list:
    favorite_list.append(row.id)