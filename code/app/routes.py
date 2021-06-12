from app import app, classes, db
from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from flask_login import current_user, login_user, login_required, logout_user

# from flask import Flask
import os

team_list = [
    {'name': 'Kyle Brook', 'title': "CEO"},
    {'name': 'Trevor Santiago', 'title': "CTO"},
    {'name': 'Efrem Ghebreab', 'title': "Data Scientist"},
    {'name': 'Wonseok Choi', 'title': "Software Engineer"},
    {'name': 'Anni Liu ', 'title': "Data Scientist"},
    {'name': 'Dawn(shuyan Li)', 'title': "Software Engineer"},
    {'name': 'Janson(Ye Tao)', 'title': "Data Scientist"}
]


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
    return render_template('about.html')


@app.route('/team')
def team():
    """
    teams page
    """
    return render_template('team.html', names=team_list)


class UploadFileForm(FlaskForm):
    """
    Class for uploading file when submitted
    """
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Upload a file from a client machine
    """
    file = UploadFileForm()  # file : UploadFileForm class instance
    if file.validate_on_submit():  # Check if it is a POST request and if it is valid.
        f = file.file_selector.data  # f : Data of FileField
        filename = f.filename
        # filename : filename of FileField

        file_dir_path = os.path.join(app.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)
        # Save file to file_path (instance/ + 'files’ + filename)
        f.save(file_path)

        return redirect(url_for('index'))  # Redirect to / (/index) page.
    return render_template('upload.html', form=file)


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
    return render_template('register.html', form=registration_form)


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

    return render_template('login.html', form=login_form)


@app.route('/')
def logout():
    """
    Log out
    """
    return render_template('index.html')