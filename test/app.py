import base64
from io import BytesIO

import numpy as np
import requests
from PIL import Image
from flask import Flask
from flask import jsonify, render_template

import model as m

app = Flask(__name__)

classes = '2346789abcdefghjmnpqrtuxyzABCDEFGHJMNPQRTUXYZ'


def predict():
    url = 'http://api.shuibei.chxj.name/captcha'

    response = requests.get(url)
    bytes_io = BytesIO(response.content)
    img = Image.open(bytes_io).convert('RGB')

    arr = np.array(img)

    char1 = arr[0:36, 0:30]
    char2 = arr[0:36, 30:60]
    char3 = arr[0:36, 60:90]
    char4 = arr[0:36, 90:120]

    model = m.build((36, 30, 3), len(classes))
    input = np.array([char1, char2, char3, char4])
    predict = model.predict(input)

    text = ''
    for i in np.argmax(predict, axis=1):
        text += classes[i]

    print("the image is", text)
    return {'image': base64.b64encode(bytes_io.getvalue()).decode(), 'text': text}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch')
def fetch():
    return jsonify(predict())
