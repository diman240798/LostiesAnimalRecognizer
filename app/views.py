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


@app.route('/get_type', methods=['GET', 'POST'])
def get_type_animal_string():
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_name = str(uuid.uuid1()) + "_" + str(time.time()) + ".png"
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


def getPhoto(animal):
    imagePath = IMAGES_DIR + animal.type_animal + "/" + animal.name_photo
    in_file = open(imagePath, "rb")  # opening for [r]eading as [b]inary
    data = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()
    return data


def get_rand_animal_from_list(animals, session):
    rand = random.randrange(0, animals.count())
    animal = animals[rand]
    animal_schema = AnimalSchema()
    response = animal_schema.dump(animal)
    data = getPhoto(animal)
    response['photo'] = list(data)
    return response


@app.route('/get_rand_animal', methods=['GET'])
def get_rand_animal():
    session = db.session
    animals = session.query(Animal)
    response = get_rand_animal_from_list(animals, session)
    session.close()
    return jsonify(response)


@app.route('/get_rand_cat', methods=['GET'])
def get_rand_cat():
    session = db.session
    animals = session.query(Animal).filter(Animal.type_animal == TYPE_CAT)
    response = get_rand_animal_from_list(animals, session)
    session.close()
    return response


@app.route('/get_rand_dog', methods=['GET'])
def get_rand_dog():
    session = db.session
    animals = session.query(Animal).filter(Animal.type_animal == TYPE_DOG)
    response = get_rand_animal_from_list(animals, session)
    session.close()
    return response


@app.route('/rate_animal', methods=['POST'])
def rate_animal():
    name_photo = request.values['name_photo']  # запрос к данным формы
    like = request.values['liked']
    session = db.session
    animal: Animal = session.query(Animal).get(name_photo)
    if animal is not None:
        if like is not None:
            animal.count_liked += 1
        else:
            animal.count_unliked += 1
        session.add(animal)
        session.commit()
        session.close()
        return "ok"
    return "animal not found"
