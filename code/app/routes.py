from app import app, classes, db
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user

import os
import sys

from predict import pred


@app.route('/')
def index():
    """
    Home page
    """
    return render_template('index.html', authenticated_user=current_user.is_authenticated)


@app.route('/about')
def about():
    """
    About page
    """
    return render_template('about.html', authenticated_user=current_user.is_authenticated)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Upload a file from a client machine
    """
    file = classes.UploadFileForm()  # file : UploadFileForm class instance
    if file.validate_on_submit():  # Check if it is a POST request and if it is valid.
        f = file.file_selector.data  # f : Data of FileField
        filename = f.filename
        # filename : filename of FileField
        file_dir_path = os.path.join(app.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)
        # Save file to file_path (instance/ + 'files’ + filename)
        f.save(file_path)
        result = pred(file_path)  # run prediction on input data
        os.remove(file_path)
        output = 'Our Prediction:'
        result = f'"{result.title()}"'
        return render_template('upload.html', form=file, result=result.title(), output=output)  # Redirect to / (/index) page.
    return render_template('upload.html', form=file, authenticated_user=current_user.is_authenticated)

@app.route('/register',  methods=('GET', 'POST'))
def register():
    """
    Registration form
    """
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count() \
            + classes.User.query.filter_by(email=email).count()
        if user_count > 0:
            flash('Error - Existing user : ' + username
                   + ' OR ' + email)
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('page-register.html', form=registration_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = classes.User.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username and password combination')

    return render_template('page-login.html', form=login_form)


@app.route('/logout')
def logout():
    """
    Log out
    """
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(401)
def re_route(e):
    return redirect(url_for('login'))


@app.errorhandler(403)
def re_route(e):
    return render_template('page-403.html')


@app.errorhandler(404)
def re_route(e):
    return render_template('page-404.html')


@app.errorhandler(500)
def re_route(e):
    return render_template('page-500.html')



