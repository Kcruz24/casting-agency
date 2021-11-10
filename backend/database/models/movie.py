from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()


class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()

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
