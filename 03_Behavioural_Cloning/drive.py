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


if __name__ == '__main__':
    model = load_model('self-driving-model.h5')
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
