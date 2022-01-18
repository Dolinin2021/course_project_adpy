import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DSN = 'postgresql+psycopg2://ilya:12345@localhost:5432/adpy_course_project'
Base = declarative_base()
engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


class BanList(Base):
    __tablename__ = 'ban_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)


class FavoriteList(Base):
    __tablename__ = 'favorite_list'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)