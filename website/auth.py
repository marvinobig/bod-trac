from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        return render_template('login.html')
    


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')
        startingBw = request.form.get('startingBw')

        try:
            if len(username) < 4:
                flash('Username is too short, must be greater than 4 letters', category='error')
            elif len(email) < 4:
                flash('Email is too short, must be greater than 4 letters', category='error')
            elif password != passwordConfirm:
                flash('Password does not match', category='error')
            elif len(password) < 8:
                flash('Password is too short, must be longer than 8 characters', category='error')
            else:
                newUser = User(username=username, email=email, password=generate_password_hash(password, method='sha256'), startingBw=startingBw)
                db.session.add(newUser)
                db.session.commit()
                flash('Account created', category='success')
                return redirect(url_for('auth.login'))
        except IntegrityError:
            flash('Email already exists, use another one', category='error')
            return render_template('signup.html')


@auth.route('/logout')
def logout():
    return '<h1>Hello Logout</h1>'
