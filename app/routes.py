from app import app
from flask import render_template 
# from flask import Flask 
# import os 

team_list = [ 'Kyle', 'Trevor', 'Efrem', 'Choi', 'Anni', 'Dawn', 'Ye Tao', 'Binaya']



@app.route('/')
def index():
	"""deployment of home page html"""
	return render_template('index.html')


@app.route('/about')
def about():
	"""deployment of about page html"""
	return render_template('about.html')


@app.route('/team')
def team():
	"""deployment of team page html"""
	return render_template('team.html', names=team_list)
