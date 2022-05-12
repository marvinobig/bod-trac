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

                label = []
                weight = []

                for recordedBw in current_user.recordedBws:
                    label.append(json.dumps(recordedBw.currentDate.strftime('%d %b')))
                    weight.append(json.dumps(float(recordedBw.bW)))
                    
                return render_template('account.html', currentUser = current_user, label=label, weight=weight)
            else:
                flash('Incorrect email or password', category='error')
                return render_template('login.html', currentUser = current_user)
        else:
            flash('No account with those details exists', category='error')
            return render_template('login.html', currentUser = current_user)
    

@auth.route('/account')
@login_required
def account_page():
    label = []
    weight = []

    for recordedBw in current_user.recordedBws:
        label.append(json.dumps(recordedBw.currentDate.strftime('%d %b')))
        weight.append(json.dumps(float(recordedBw.bW)))

    return render_template('account.html', currentUser = current_user, label=label, weight=weight)


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
                return render_template('signup.html', currentUser = current_user)
            elif len(username) < 4:
                flash('Username is too short, must be greater than 4 letters', category='error')
                return render_template('signup.html', currentUser = current_user)
            elif len(email) < 4:
                flash('Email is too short, must be greater than 4 letters', category='error')
                return render_template('signup.html', currentUser = current_user)
            elif password != passwordConfirm:
                flash('Password does not match', category='error')
                return render_template('signup.html', currentUser = current_user)
            elif len(password) < 8:
                flash('Password is too short, must be longer than 8 characters', category='error')
                return render_template('signup.html', currentUser = current_user)
            else:
                newUser = User(username=username, email=email, password=generate_password_hash(password, method='sha256'), startingBw=startingBw)
                db.session.add(newUser)
                db.session.commit()
                flash('Account created', category='success')
                return redirect(url_for('auth.login'))
        except IntegrityError:
            flash('Email already exists, use another one', category='error')
            return render_template('signup.html', currentUser = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You\'ve been logged out", category='success')
    return redirect(url_for('auth.login'))


@auth.route('/deleteAccount', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'GET':
        return render_template('delete.html', currentUser = current_user)
    else:
        password = request.form.get('password')

        if check_password_hash(current_user.password, password):
            deleteUser = User.query.filter(User.id == current_user.id).one()
            userData = BodyWeight.query.filter(BodyWeight.user_id == current_user.id).all()

            if userData:
                for data in userData:
                    db.session.delete(data)
                    db.session.commit()
                
            
            flash(f'The account belonging to {current_user.username} has been deleted', category='success')
            db.session.delete(deleteUser)
            db.session.commit()
            logout_user()
            return render_template('home.html', currentUser = current_user)
        else:
            flash('Incorrect password', category='error')
            return render_template('delete.html', currentUser = current_user)