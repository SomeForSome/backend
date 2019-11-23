from flask import Flask
from flask_cors import CORS
from config import Config

UPLOAD_FOLDER = './photos'

app = Flask(__name__)
CORS(app, resources={r'/.*': {'origins': '*'}})
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == '__main__':
    app.run()
