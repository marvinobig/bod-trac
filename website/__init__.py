import sqlite3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'bod-trac.db'


def page_not_found(e):
    return render_template('error.html'), 404


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dtfbawlowg'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_error_handler(404, page_not_found)
    
    from .models import User, BodyWeight

    create_database(app)

    return app
    

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database Created!')