import socketio
import eventlet
from flask import Flask
import numpy as np
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2

sio = socketio.Server()

app = Flask(__name__)  # '__main__' name
speed_limit = 10


def img_preprocess(img):
    img = img[60:135, :, :]  # shortening height of image [height, width, layer]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  # image space used for training NVIDIA neural model
    img = cv2.GaussianBlur(img, (3, 3), 0)  # smoothening image technique
    img = cv2.resize(img, (200, 66))  # resizing image as per specifications of NVIDIA neural model
    img = img / 255  # normalizing image (reduce variance btw image data without visual impact)
    return img





if __name__ == '__main__':
    model = load_model('self-driving-model.h5')
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
