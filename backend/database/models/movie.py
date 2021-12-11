from sqlalchemy import Column, Integer, String, Date
from backend.entitites.model import Model


class Movie(Model):
    id: int
    title: String
    release_date: Date

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return f'<id: {self.id},' \
               f'title: {self.title},' \
               f'release_date: {self.release_date}>'
