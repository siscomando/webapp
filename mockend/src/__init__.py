# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
# import flask_debugtoolbar

# Config. To separate this when you needing by using config.from_object
 # See more #1
app.config['SECRET_KEY'] = '$3cr0to'
app.config['DEBUG'] = True
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'default'

if app.config['DEBUG']:
	# purpose tests
    app.config['MONGODB_SETTINGS'] = {'db':'test_mockend'}
else:
	# production
    app.config['MONGODB_SETTINGS'] = {'db':'mockend'}

database = MongoEngine(app)

# Config cans to be used: app.config.from_object(__name__)
# from_object() will look at the given object (if it’s a string it will import it) 
# and then look for all uppercase variables defined there.
# or
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Load views
from src import views

if __name__ == '__main__':
    app.run()


#1 See more https://flask-mongoengine.readthedocs.org/en/latest/