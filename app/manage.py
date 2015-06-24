# -*- coding: utf-8 -*-
from flask.ext.script import Manager, Server
#from tornado.wsgi import WSGIContainer
#from tornado.httpserver import HTTPServer
#from tornado.ioloop import IOLoop 
#APP
from siscomando import app

#http_server = HTTPServer(WSGIContainer(app))
#http_server.listen(9003)
#IOLoop.instance().start()
manager = Manager(app)
manager.add_command('runserver', Server(host='127.0.0.1', port=9003))
	
if __name__ == '__main__':
	# IOLoop.instance().start()
	manager.run()

