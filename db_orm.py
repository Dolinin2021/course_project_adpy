import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
DSN = 'postgresql+psycopg2://Ilya:12345@localhost:5432/adpy_course_project'

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)


class Profile(Base):
    __tablename__ = 'profile'

    id = sq.Column(sq.Integer, primary_key=True)
    profile_id = sq.Column(sq.Integer, unique=True)


class UserToProfile(Base):
    __tablename__ = 'user_to_profile'

    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'))
    profile_id = sq.Column(sq.Integer, sq.ForeignKey('profile.id'))
    favorite = sq.Column(sq.String)
    is_banned = sq.Column(sq.String)


# class Artist(Base):
#     __tablename__ = 'artist'
#
#     id = sq.Column(sq.Integer, primary_key=True)
#     name = sq.Column(sq.String, nullable=False, unique=True)
#     albums = relationship('Album', back_populates='artist')
#
#
# class Album(Base):
#     __tablename__ = 'album'
#
#     id = sq.Column(sq.Integer, primary_key=True)
#     title = sq.Column(sq.String)
#     tracks = relationship('Track', backref='album',  cascade="all,delete")
#     published = sq.Column(sq.Date)
#     id_artist = sq.Column(sq.Integer, sq.ForeignKey('artist.id'))
#     artist = relationship(Artist)
#
#
# class Genre(Base):
#     __tablename__ = 'genre'
#
#     id = sq.Column(sq.Integer, primary_key=True)
#     title = sq.Column(sq.String)
#     tracks = relationship('Track', secondary='track_to_genre', back_populates='genres', cascade="all,delete")
#
#
# class Track(Base):
#     __tablename__ = 'track'
#
#     id = sq.Column(sq.Integer, primary_key=True)
#     title = sq.Column(sq.String)
#     duration = sq.Column(sq.Integer, nullable=False)
#     genres = relationship(Genre, secondary='track_to_genre', back_populates='tracks', cascade="all,delete")
#     id_album = sq.Column(sq.Integer, sq.ForeignKey('album.id', ondelete="CASCADE"))
#
#     # @classmethod
#     # def get_all(cls):
#     #     session = Session()
#     #     return session.query(cls).all()
#
#
#
# track_to_genre = sq.Table(
#     'track_to_genre', Base.metadata,
#     sq.Column('genre_id', sq.Integer, sq.ForeignKey('genre.id', ondelete="NO ACTION")),
#     sq.Column('track_id', sq.Integer, sq.ForeignKey('track.id', ondelete="CASCADE")),
# )
#
#
# if __name__ == '__main__':
#     session = Session()
#     # Init scheme
#     Base.metadata.create_all(engine)
#
#     # Example data
#     date_ar1 = {
#         'Best Album 1': [
#             {'name': 'Audio 1_1', 'dur': 61},
#             {'name': 'Audio 1_2', 'dur': 32},
#             {'name': 'Audio 1_3', 'dur': 43}
#         ],
#         'Best Album 2': [
#             {'name': 'Audio 2_1', 'dur': 62},
#             {'name': 'Audio 2_2', 'dur': 32},
#             {'name': 'Audio 2_3', 'dur': 42}
#         ]
#     }
#     # Example 1
#     new_artist = Artist(name="Artist 2")
#
#     for name_alb, track_list in date_ar1.items():
#         new_album = Album(title=name_alb, artist=new_artist)
#         tracks = []
#         for track_raw in track_list:
#             _track = Track(title=track_raw['name'], duration=track_raw['dur'])
#             _track.album = new_album
#             tracks.append(_track)
#         session.add_all(tracks)
#
#     # Example 2
#     g1 = Genre(title='blues')
#     g2 = Genre(title='jazz')
#     tracks = session.query(Track).filter(Track.duration <= 45).all()
#     for track in tracks:
#         track.genres.append(g1)
#
#     album = session.query(Album).filter_by(title="Best Album 2").first()
#     for track in album.tracks:
#         track.genres.append(g2)
#         track.title = f"{track.title} Jazz"
#
#     # Example 3
#     # Update need use synchronize_session(!):
#     # query = (
#     #     session.query(Track)
#     #         .filter(Track.title.ilike("%_3"))
#     #         .filter(Track.duration == 42)
#     #         .update({"duration": 66}, synchronize_session=False)
#     # )
#     # Delete use ondelete="CASCADE" in ForeignKey:
#     # session.query(Track).filter_by(title="Audio 2_2").delete()
#     session.commit()
#
#     # Example 4 add custom method
#     # print(Track.get_all())
#     print('Finish')