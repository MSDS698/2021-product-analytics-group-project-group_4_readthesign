from app import app, classes, db
from flask import render_template,redirect, url_for
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
		{'name': 'Winseok Choi', 'title': "Software Engineer"},
		{'name': 'Anni Liu ', 'title': "Data Scientist"},
		{'name': 'Dawn(shuyan Li)', 'title': "Software Engineer"},
		{'name': 'Janson(Ye Tao)', 'title': "Data Scientist"}
]

# --------------------------------
# Home page 
# --------------------------------
@app.route('/')
def index():
	return render_template('index.html')

# --------------------------------
# about page
# --------------------------------
@app.route('/about')
def about():
	return render_template('about.html')

# --------------------------------
# our teams page
# --------------------------------
@app.route('/team')
def team():
	return render_template('team.html', names=team_list)
# --------------------------------
# Service route
# --------------------------------
@app.route('/services')
def services():
	return render_template('services.html')
# --------------------------------
# Clients route
# --------------------------------
@app.route('/clients')
def clients():
	return render_template('clients.html')

# --------------------------------
# file uploading
# --------------------------------
class UploadFileForm(FlaskForm):
    """Class for uploading file when submitted"""
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """upload a file from a client machine."""
    file = UploadFileForm()  # file : UploadFileForm class instance
    if file.validate_on_submit():  # Check if it is a POST request and if it is valid.
        f = file.file_selector.data  # f : Data of FileField
        filename = f.filename
        # filename : filename of FileField

        file_dir_path = os.path.join(app.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)
        f.save(file_path) # Save file to file_path (instance/ + 'files’ + filename)

        return redirect(url_for('index'))  # Redirect to / (/index) page.
    return render_template('upload.html', form=file)


# --------------------------------
# Regsitration form 
# --------------------------------

@app.route('/register',  methods=('GET', 'POST'))
def register():
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count() \
                     + classes.User.query.filter_by(email=email).count()
        if (user_count > 0):
            return '<h1>Error - Existing user : ' + username \
                   + ' OR ' + email + '</h1>'
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('register.html', form=registration_form)

# --------------------------------
# Login form 
# --------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = classes.User.query.filter_by(username=username).first()

        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return render_template('welcome.html', form=username)
            # return("<h1> Welcome {}!</h1>".format(username))

    return render_template('login.html', form=login_form)

# --------------------------------
# Log out 
# --------------------------------
@app.route('/')
def logout():
	return render_template('index.html') 
