import sqlite3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'bod-trac'


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
    

    return app
