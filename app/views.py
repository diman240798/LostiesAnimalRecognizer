import os
import uuid
import time
import random

from flask import render_template, url_for, request, jsonify, flash, make_response
from werkzeug.utils import secure_filename
from app import full_path_photos


from models.animal import *
from app import app, db, ALLOWED_EXTENSIONS

from animal_types.label_image import classify_animal_image
import json

from constants import *


@app.route('/get_type', methods=['POST'])
def get_type_animal():
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file_name = str(uuid.uuid1()) + "_" + str(time.time()) + "." + file_name.split('.')[1]
            file.save(TEMP_PATH + file_name)  # сохраняем файл

            classified = classify_animal_image(TEMP_PATH + file_name)
            if classified == TYPE_CAT:
                os.rename(TEMP_PATH + file_name, CATS_PATH + file_name)
            elif classified == TYPE_DOG:
                os.rename(TEMP_PATH + file_name, DOGS_PATH + file_name)
            else:
                os.rename(TEMP_PATH + file_name, OTHERS_PATH + file_name)

            return classified
    except FileNotFoundError as e:
        print(e)
        flash("Ошибка чтения файла", "error")  # всплывающее сообщение
    return 'unknown'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# @app.route('/', methods=['GET'])
# def home_page():
#     return render_template("index.html")


def getPhoto(animal):
    imagePath = IMAGES_DIR + animal.type_animal + "/" + animal.name_photo
    in_file = open(imagePath, "rb")  # opening for [r]eading as [b]inary
    data = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()
    return data


@app.route('/get_rand_animal', methods=['GET'])
def get_rand_animal():
    session = db.session
    animals = session.query(Animal)
    rand = random.randrange(0, animals.count())
    animal = animals[rand]
    session.close()
    response = AnimalRequest(getPhoto(animal), animal.count_liked, animal.count_unliked, animal.type_animal)
    return response.toJSON()


@app.route('/get_rand_cat', methods=['POST'])
def get_rand_cat():
    session = db.session
    animals = session.query(Animal).filter_by(type_animal = TYPE_CAT)
    rand = random.randrange(0, animals.count())
    animal = animals[rand]
    session.close()
    return animal


@app.route('/get_rand_dog', methods=['POST'])
def get_rand_dog():
    session = db.session
    animals = session.query(Animal).filter_by(type_animal = TYPE_DOG)
    rand = random.randrange(0, animals.count())
    animal = animals[rand]
    session.close()
    return animal


@app.route('/rate_animals', methods=['POST'])
def rate_animals():
    name_photo = request.form.get('img_animal')  # запрос к данным формы
    like = request.form.get('like')
    session = db.session
    if like is not None:
        animal: Animal = session.query(Animal).get(name_photo)
        animal.count_liked += 1
        session.add(animal)
        session.commit()
    else:
        animal: Animal = session.query(Animal).get(name_photo)
        animal.count_unliked += 1
        session.add(animal)
        session.commit()
    session.close()
    # return render_template("rate_animal.html", data=json.dumps(full_path_photos))


# @app.route('/about_animals', methods=['GET'])
# def about_animal():
#     return render_template("about_animals.html", data=json.dumps(full_path_photos))
