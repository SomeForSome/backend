
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os

from EmoPy.src.fermodel import FERModel


UPLOAD_FOLDER = './photos'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r'/.*': {'origins': '*'}})

emotions = ['happiness', 'anger', 'calm']
model = FERModel(emotions, verbose=True)

@app.route('/', methods=['POST'])
@cross_origin(origin='*')
def determine():
    if not 'file' in request.files:
        return jsonify({'error': 'no file'}), 400
    # Image info
    img_file = request.files['file']
    img_name = secure_filename(img_file.filename)
    # Write image to static directory
    img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
    res = model.predict(app.config['UPLOAD_FOLDER'] + '/' + img_name)
    if res['happiness'] > 60:
        return '1'
    if res['anger'] > 50:
        return '2'
    else:
        return '3'


if __name__ == '__main__':
    app.run()
