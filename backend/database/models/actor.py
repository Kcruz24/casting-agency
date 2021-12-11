from sqlalchemy import Column, Integer, String

from backend.entitites.model import Model


class Actor(Model):
    id: int
    name: String
    age: int
    gender: String

    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f'<id: {self.id}, ' \
               f'name: {self.name}, ' \
               f'age: {self.age}, ' \
               f'gender: {self.gender}>'
