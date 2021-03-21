import os

IMAGES_DIR = "app/static/photos/"
CATS_PATH = IMAGES_DIR + "cat/"
DOGS_PATH = IMAGES_DIR + "dog/"
OTHERS_PATH = IMAGES_DIR + "other/"
TEMP_PATH = IMAGES_DIR + "temp/"


os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CATS_PATH, exist_ok=True)
os.makedirs(DOGS_PATH, exist_ok=True)
os.makedirs(OTHERS_PATH, exist_ok=True)
os.makedirs(TEMP_PATH, exist_ok=True)