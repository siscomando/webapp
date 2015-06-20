import os

# app settings
DEBUG = True
TESTING = False

# email settings
ADMINS = ['horacioibrahim@gmail.com']
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# database settings 
if TESTING:
	# purpose tests
    MONGODB_SETTINGS = {'db':'test_mockend'}
else:
	# production
    MONGODB_SETTINGS = {'db':'mockend'}
