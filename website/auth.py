from flask import Blueprint, render_template, request, flash

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
        userName = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        if len(userName) < 4:
            flash('Username is too short, must be greater than 4 letters', category='error')
        elif len(email) < 4:
            flash('Email is too short, must be greater than 4 letters', category='error')
        elif password != passwordConfirm:
            flash('Password does not match', category='error')
        elif len(password) < 8:
            flash('Password is too short, must be longer than 8 characters', category='error')
        else:
            flash('Account created', category='success')
            #add user to database
 
        return render_template('signup.html')


@auth.route('/logout')
def logout():
    return '<h1>Hello Logout</h1>'
