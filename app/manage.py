# -*- coding: utf-8 -*-
from flask.ext.script import Manager, Server, Command, Option, Shell
#APP
from siscomando import app
#from api import app as app_api


class GunicornServer(Command):
	""" This class was based in http://stackoverflow.com/a/14569881/2283488.
	"""
	description = 'Run the app within Gunicorn'

	def __init__(self, host='127.0.0.1', port=9010, workers=4,
		worker_class='gunicorn.workers.ggevent.GeventWorker'):
		self.port = port
		self.host = host
		self.workers = workers
		self.worker_class = worker_class

	def get_options(self):
		return (
			Option('-H', '--host', dest='host', default=self.host),
			Option('-p', '--port', type=int, default=self.port),
			Option('-w', '--workers', type=int, default=self.workers),
			Option('-wc', '--worker-class', dest='worker_class', default=self.worker_class),
		)

	def __call__(self, app, host, port, workers, worker_class):
		from gunicorn.app.base import Application

		class FlaskApplication(Application):
			def init(self, parser, opts, args):
				""" This configures the Application class from gunicorn.
				"""
				#self.args = args
				#self.app = app
				# port = 9013

				#if 'runserver_api' in self.args:
				#	port = 9014 # to allow run both instances.
				#	self.app = app_api


				return {
					'bind': '{0}:{1}'.format(host, port),
					'workers': workers,
					'worker_class': worker_class,
				}

			def load(self):
				return app

		FlaskApplication().run()


manager = Manager(app)
# `runserver_sync` runs the server as develop mode from flask.
manager.add_command('runserver_sync', Server(host='127.0.0.1', port=9010))
# `runserver` runs the server of the WebApp for production behavior.
manager.add_command('runserver', GunicornServer())
# `runserver_api` runs the server of the API for production behavior.
#manager.add_command('runserver_api', GunicornServer())


if __name__ == '__main__':
	# IOLoop.instance().start()
	manager.run()
