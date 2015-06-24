from config import *

# Usage
# export SISCOMANDO_SETTINGS enviroment variable with path of the config
# e.g.: export SISCOMANDO_SETTINGS=/path/to/config.py
DEBUG = True
# app settings
SECRET_KEY = '$3cr0to'
USERNAME = 'admin'
PASSWORD = 'default'

# email settings
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# email settings
ADMINS = ['horacioibrahim@gmail.com']
#### AMAZON SES SAMPLE ######
MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_DEFAULT_SENDER = 'team@hipy.co'
#AWS_SES_RETURN_PATH = 'ADDRESS_TO_REPLY'
AWS_ACCESS_KEY_ID = 'AKIAJF4SNXPIZUQVTYOA'
AWS_SECRET_ACCESS_KEY = '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'

