from serv import app, db
from serv.db import InvalidRequestError
from werkzeug.utils import secure_filename
from flask import request, jsonify
from flask_cors import cross_origin
from serv.emo_rec import models
import hashlib
import os

emotions = {
    'sad': '😞',
    'depressed': '😩',
    'neutral': '😐',
    'glad': '😀',
    'happy': '😁',
    'angry': '😡',
    'astonished': '😦',
    'surprise': '😮'
}

BLOCK_SIZE = 65536


def determine(path):
    values = [model.predict(path) for model in models]
    result = 0
    if abs(values[0]['angry'] - values[0]['happiness']) < 30:
        result = 'neutral'
    elif values[0]['angry'] > values[0]['happiness']:
        if values[0]['angry'] > 75:
            result = 'angry' if values[1]['sad'] < 40 else 'depressed'
        else:
            result = 'sad'
    else:
        if values[2]['surprise'] < 30:
            result = 'glad' if values[0]['happiness'] < 80 else 'happy'
        else:
            result = 'astonished' if values[2]['surprise'] < 50 else 'surprise'
    return result


def file_to_hash(file):
    file_hash = hashlib.sha256()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)

    return file_hash.hexdigest()


@app.route('/', methods=['POST'])
@cross_origin(origin='*')
def push():
    if not 'file' in request.files:
        return jsonify({'error': 'no file'}), 400
    img_file = request.files['file']
    img_name = secure_filename(img_file.filename)
    img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))

    hashcode = file_to_hash(app.config['UPLOAD_FOLDER'] + '/' + img_name)
    os.remove(app.config['UPLOAD_FOLDER'] + '/' + img_name)

    try:
        does_exist = db.check_query(hashcode)
    except InvalidRequestError:
        return jsonify({'error': 'db_error'}), 400

    if not does_exist:  # )))
        img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], hashcode))
        resp = determine(app.config['UPLOAD_FOLDER'] + '/' + img_name)
    else:
        resp = does_exist

    return jsonify({'resp': resp}), 200
