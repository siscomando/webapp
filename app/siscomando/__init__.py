# -*- coding: utf-8 -*-
from __future__ import absolute_import
import redis
from flask import Flask, Blueprint 
from flask.ext.mongoengine import MongoEngine
from flask.ext.cors import CORS
from flask.ext.login import LoginManager
from flask_mail import Mail
from flask.ext.babel import Babel
from flask.ext import restful

# Pre-setup
red = redis.StrictRedis()

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='{#',
        comment_end_string='#}'
    ))


app = CustomFlask(__name__)
app.config.from_envvar('SISCOMANDO_SETTINGS')

# Settings webservice flask_restful entry point.
webservice_bp = Blueprint('webservice', __name__)
webservice = restful.Api(webservice_bp, prefix="/api/v2")

# CORS to support external request (outside from hosted domain).
cors = CORS(app, resources=r'/api/v1/*', origins='*', 
	allow_headers=['Content-Type', 'Origin', 'Accept,', 'X-Requested-With', 
				'X-CSRF-Token','Access-Control-Allow-Origin'])
# Mail
mail = Mail(app)
# i18n and l10n
babel = Babel(app)

# Load together Flask and Flask-login.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

database = MongoEngine(app)

# Config cans to be used: app.config.from_object(__name__)
# from_object() will look at the given object (if it’s a string it will import it) 
# and then look for all uppercase variables defined there.
# Load views
from siscomando import views

if __name__ == '__main__':
    app.run(threaded=True) #


#1 See more https://flask-mongoengine.readthedocs.org/en/latest/
