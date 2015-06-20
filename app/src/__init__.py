# -*- coding: utf-8 -*-
import redis
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.cors import CORS
from flask.ext.login import LoginManager
from flask_mail import Mail
from flask.ext.babel import Babel

# Pre-setup
red = redis.StrictRedis()

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>'
    ))


#app = Flask(__name__)
app = CustomFlask(__name__)
app.config.from_envvar('SISCOMANDO_SETTINGS')

cors = CORS(app, resources=r'/api/*', origins='*', 
	allow_headers=['Content-Type', 'Origin', 'Accept,', 'X-Requested-With', 
				'X-CSRF-Token','Access-Control-Allow-Origin'])

# Mail
mail = Mail(app)
# i18n and l10n
babel = Babel(app)

# Load together Flask and Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

database = MongoEngine(app)

# Config cans to be used: app.config.from_object(__name__)
# from_object() will look at the given object (if it’s a string it will import it) 
# and then look for all uppercase variables defined there.
# or
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Load views
from src import views

if __name__ == '__main__':
    app.run(threaded=True) #


#1 See more https://flask-mongoengine.readthedocs.org/en/latest/