from serv import app
from werkzeug.utils import secure_filename
from flask import request, jsonify
from flask_cors import cross_origin
from serv.emo_rec import models
import os


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
    for model in models:
        model.predict(app.config['UPLOAD_FOLDER'] + '/' + img_name)
    return jsonify({'resp': 'OK'}), 200
