import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


with open('dsn.txt', 'r', encoding='utf-8') as file_obj:
    DSN = file_obj.read().strip()

Base = declarative_base()
engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

ban_list = []
favorite_list = []
unique_list = []


class UniqueList(Base):
    """Пользователи, которые были найдены в результате поиска и не должны выводиться при повторном поиске."""
    __tablename__ = 'unique_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


class BanList(Base):
    """Пользователи, которых добавили в чёрный список."""
    __tablename__ = 'ban_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


class FavoriteList(Base):
    """Пользователи, которых добавили в список 'Избранное'."""
    __tablename__ = 'favorite_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


Base.metadata.create_all(engine)


query_value_unique_list = session.query(UniqueList).all()
for row in query_value_unique_list:
    unique_list.append(row.id)

query_value_ban_list = session.query(BanList).all()
for row in query_value_ban_list:
    ban_list.append(row.id)

query_value_favorite_list = session.query(FavoriteList).all()
for row in query_value_favorite_list:
    favorite_list.append(row.id)