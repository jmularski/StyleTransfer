from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from models.model import StyleTransfer
from PIL import Image
from matplotlib.pyplot import savefig, imshow
import numpy as np
from cStringIO import StringIO
import base64
app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
socket = SocketIO(app)
CORS(app)

model = StyleTransfer()
model.initialize_model()

@socket.on('predict')
def on_predict(data):
    photos = data
    image = model.preprocess_images(photos[1], photos[0])
    for i in range(100):
        data_image = StringIO()
        model.train_step(image)
        result_image = image.read_value()[0]
        imshow(result_image)
        savefig(data_image, format='png')
        socket.emit('image', base64.encodestring(data_image.getvalue()))
        socket.emit('progress', i + 1)


if __name__ == "__main__":
    app.run()