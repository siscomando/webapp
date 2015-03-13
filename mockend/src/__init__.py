from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB':'mockend'}
app.config['SECRET_KEY'] = '$3cr0to'

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
