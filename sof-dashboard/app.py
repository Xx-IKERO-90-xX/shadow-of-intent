import os
import sys
import json
from datetime import datetime
from flask import request, Flask, render_template, redirect, session, sessions, url_for
from werkzeug.utils import secure_filename
import asyncio
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_socketio import SocketIO


settings = {}
with open("settings.json") as setting:
    settings = json.load(setting)

app = Flask(__name__)
app.secret_key = "a40ecfce592fd63c8fa2cda27d19e1dbc531e946"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{settings['mysql']['user']}:{settings['mysql']['passwd']}@{settings['mysql']['host']}/{settings['mysql']['db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context()

socketio = SocketIO(app, async_mode='eventlet')


from routes import *

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(repo_bp)
app.register_blueprint(elink_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    socketio.run(
        app,
        host=settings['flask']['host'],
        port=settings['flask']['port'],
        debug=settings['flask']['debug'],
        allow_unsafe_werkzeug=True
    )