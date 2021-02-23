from flask import Flask, request
import os, time, uuid
from animal_types.label_image import classify_animal_image

IMAGES_PATH = "./photos"
CATS_PATH = IMAGES_PATH + "/cats"
DOGS_PATH = IMAGES_PATH + "/dogs"
OTHERS_PATH = IMAGES_PATH + "/others"
TEMP_PATH = IMAGES_PATH + "/temp"

os.makedirs(IMAGES_PATH, exist_ok=True)
os.makedirs(CATS_PATH, exist_ok=True)
os.makedirs(DOGS_PATH, exist_ok=True)
os.makedirs(OTHERS_PATH, exist_ok=True)
os.makedirs(TEMP_PATH, exist_ok=True)

app = Flask(__name__)


@app.route('/get_type', methods=['POST'])
def hello_world():
    fileName = str(uuid.uuid1()) + "_" + str(time.time()) + ".jpg"
    tempPath = TEMP_PATH + "/" + fileName
    request.files.get('imagefile', '').save(tempPath)
    classified = classify_animal_image(tempPath)
    if classified == 'cat':
        os.replace(tempPath, CATS_PATH + "/" + fileName)
    elif classified == 'dog':
        os.replace(tempPath, DOGS_PATH + "/" + fileName)
    else:
        os.replace(tempPath, OTHERS_PATH + "/" + fileName)

    return classified
