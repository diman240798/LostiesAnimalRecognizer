from app import db, ma

TYPE_DOG = 'dog'
TYPE_CAT = 'cat'
TYPE_OTHER = 'other'


class Animal(db.Model):
    __tablename__ = 'photo_animals'
    name_photo = db.Column(db.String(100), primary_key=True)
    count_liked = db.Column(db.Integer, nullable=False)
    count_unliked = db.Column(db.Integer, nullable=False)
    type_animal = db.Column(db.String(10), nullable=False)


class AnimalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Animal
        load_instance = True
