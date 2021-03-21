from app import db
from flask_serialize import FlaskSerialize

import json


TYPE_DOG = 'dog'
TYPE_CAT = 'cat'
TYPE_OTHER = 'other'

fs_mixin = FlaskSerialize(db)

class Animal(db.Model):
    __tablename__ = 'photo_animals'
    name_photo = db.Column(db.String(100), primary_key=True)
    count_liked = db.Column(db.Integer, nullable=False)
    count_unliked = db.Column(db.Integer, nullable=False)
    type_animal = db.Column(db.String(10), nullable=False)



class AnimalRequest():
    def __init__(self, photo = [], count_liked = 0, count_unliked = 0, type_animal = TYPE_OTHER):
        self.photo = photo
        self.count_liked = count_liked
        self.count_unliked = count_unliked
        self.type_animal = type_animal

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)