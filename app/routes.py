# Redirects from page to page

#Imports
from flask import request, render_template, flash, redirect, url_for
#from werkzeug.urls import url_parse
from urllib.parse import urlparse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

#Setup
@app.route('/')
@app.route('/index')
@login_required
def index ():
    user = {'username': 'Welcome to Team 2: Initiative Tracker'}
    return render_template('index.html', title='Home')

#Routes to login and checks for valid username && password
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)
    
#Logs out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
#Routes to registration page adding in a new user
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thank your for registering. Enjoy the APP!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form )


