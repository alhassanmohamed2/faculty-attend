from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import path, getcwd
from datetime import timedelta
db = SQLAlchemy()

MAIN_DB_NAME = "attend.db" 
STUDENTS_DATABASE_NAME = 'student_names.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'password'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{MAIN_DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {
    'student_names': f'sqlite:///{STUDENTS_DATABASE_NAME}'
    }
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    return app

def create_database(app):
    if not path.exists(MAIN_DB_NAME):
        with app.app_context():
            db.create_all()
    if not path.exists(STUDENTS_DATABASE_NAME):
        with app.app_context():
            db.create_all(bind_key='student_names')
