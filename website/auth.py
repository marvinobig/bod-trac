from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, BodyWeight
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('account.html', currentUser = current_user)
        else:
            return render_template('login.html', currentUser = current_user)
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        getUser = User.query.filter_by(email=email).first()

        if getUser:
            if check_password_hash(getUser.password, password):
                flash(f'Welcome {getUser.username}!', category='success')
                login_user(getUser, remember=True)
                return render_template('account.html', currentUser = current_user)
            else:
                flash('Incorrect email or password', category='error')
                return render_template('login.html')
        else:
            flash('No account with those details exists', category='error')
            return render_template('login.html')
    

@auth.route('/account')
@login_required
def account_page():
    label = [recordedBw.currentDate for recordedBw in current_user.recordedBws]
    weight = [recordedBw.bW for recordedBw in current_user.recordedBws]
    formattedDates = json.dumps(label, default=str)
    print(label)
    formattedWeight = json.dumps(weight, default=float)
    return render_template('account.html', currentUser = current_user, label=formattedDates, weight=formattedWeight)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('account.html', currentUser = current_user)
        else:
            return render_template('signup.html', currentUser = current_user)
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')
        startingBw = request.form.get('startingBw')

        getUser = User.query.filter_by(email=email).first()

        try:
            if getUser and getUser.password:
                flash('You\'ve already got an account', category='error')
                return render_template('signup.html')
            elif len(username) < 4:
                flash('Username is too short, must be greater than 4 letters', category='error')
                return render_template('signup.html')
            elif len(email) < 4:
                flash('Email is too short, must be greater than 4 letters', category='error')
                return render_template('signup.html')
            elif password != passwordConfirm:
                flash('Password does not match', category='error')
                return render_template('signup.html')
            elif len(password) < 8:
                flash('Password is too short, must be longer than 8 characters', category='error')
                return render_template('signup.html')
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
