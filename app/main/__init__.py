import os
from flask import Flask
from .entities import db, login_manager
from flask_bcrypt import Bcrypt

import pyrebase
from .config import config_by_name
from .auth import set_up_auth
from .entities.initializer.initEmotionLexicon import initializeEmotionLexiconTable

FIREBASE_CONFIG = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID')
}

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
        initializeEmotionLexiconTable()
    login_manager.init_app(app)
    flask_bcrypt.init_app(app)
    set_up_auth(app)

    return app
