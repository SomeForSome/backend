from flask import Flask
from flask_cors import CORS
from config import Config
from serv.db import DBConnector

UPLOAD_FOLDER = './photos'

app = Flask(__name__)
CORS(app, resources={r'/.*': {'origins': '*'}})

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = DBConnector(app.config)

from serv import routes
