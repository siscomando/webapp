"""
settings.py

Configuration for Flask app

"""
import os

MODE = ['DEVELOPMENT', 'DEVELOPMENTSES' 'PRODUCTION', 'TESTING']


class Config(object):
    DEBUG = True
    TESTING = False
    MODE = MODE[0]
    # PRODUCTION DATABASES
    MONGODB_SETTINGS = {'db':'dev_scdb'}     
    # MAIL SETTINGS
    ADMINS = ['horacioibrahim@gmail.com']
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False	


class Development(Config):
    DEBUG = True
    # app settings
    MODE = MODE[0]
    SECRET_KEY = '$3cr0to'
    USERNAME = 'admin'
    PASSWORD = 'default'
    # email settings
    MAIL_USERNAME = 'horacioibrahim@localhost'
    MAIL_PASSWORD = ''
    # email settings
    ADMINS = ['horacioibrahim@gmail.com']


class DevelopementSES(Development):
    # AMAZON SES SAMPLE
    MODE = MODE[1]
    MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'team@hipy.co'
    AWS_SES_RETURN_PATH = 'horacioibrahim@gmail.com'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


class Testing(Development):
    MODE = MODE[0]
    TESTING = True
    DEBUG = True
    # TESTING DATABASES 
    MONGODB_SETTINGS = {'db':'test_scdb'}     
    # TESTING MAIL SETTINGS


class Production(Config):
    MODE = MODE[2]
    DEBUG = False 
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # PRODUCTION DATABASES
    MONGODB_SETTINGS = {'db':'scdb'}     
    # PRODUCTION MAIL SETTINGS
