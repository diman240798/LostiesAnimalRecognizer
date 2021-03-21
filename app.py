import os

from sqlalchemy import exists

from app import app, full_path_photos, db
from models.animal import *


if __name__ == "__main__":

    db.create_all() # создаем таблицы в бд

    session = db.session

    for i, url_photo in enumerate(full_path_photos):
        name_photo = url_photo.split('/')[3]
        type_animal = url_photo.split('/')[2]
        if not session.query(exists().where(Animal.name_photo == name_photo)).scalar():
            animal: Animal = Animal(name_photo=name_photo, count_liked=0, count_unliked=0, type_animal=type_animal)
            session.add(animal)
            session.commit()
    session.close()

    app.run()
