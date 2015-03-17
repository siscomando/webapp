# -*- coding: utf-8 -*-
from flask.ext.script import Manager, Server
#APP
from src import app

manager = Manager(app)
manager.add_command('runserver', Server(host='127.0.0.1', port=9000))
	
if __name__ == '__main__':
	manager.run()

