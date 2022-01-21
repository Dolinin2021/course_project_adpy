import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


with open('dsn.txt', 'r', encoding='utf-8') as file_obj:
    DSN = file_obj.read().strip()

Base = declarative_base()

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
session = Session()

ban_list = []
favorite_list = []


class BanList(Base):
    """Список пользователей, которых добавили в чёрный список."""
    __tablename__ = 'ban_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


class FavoriteList(Base):
    """Список пользователей, которых добавили в список 'Избранное'."""
    __tablename__ = 'favorite_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


query_value_ban_list = session.query(BanList).all()
for row in query_value_ban_list:
    ban_list.append(row.id)

query_value_favorite_list = session.query(FavoriteList).all()
for row in query_value_favorite_list:
    favorite_list.append(row.id)