# -*- coding: utf-8 -*-
import os
import unittest
import tempfile
import json
import urllib
from flask import jsonify
#APP
from src import app, database, models

class SrcTestCase(unittest.TestCase):

	def setUp(self):
		app.config['DEBUG'] = True
		self.dbname = app.config['MONGODB_SETTINGS']['db']
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		self.app = app.test_client()
		self.issue_default = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'Problema de autenticação no sistema',
			'register': '2015RI/0000124',
			'ugat': 'SUPOP',
			'ugser': 'SUPGS', 
		}		

	def tearDown(self):
		db = database.connect(self.dbname)
		db.drop_database(self.dbname)

	# REST API TESTS
	def test_url_api_issues_POST(self):
		params = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'Problema de autenticação no sistema',
			'register': '2015RI/0000124',
			'ugat': 'SUPOP',
			'ugser': 'SUPGS', 
		}
		headers = [('Content-Type', 'application/json')]
		json_data = json.dumps(params)
		json_data_length = len(json_data)
		headers.append(('Content-Length', json_data_length))
		res = self.app.post('/issues/', data=json_data, content_type='application/json',
			content_length=json_data_length)
		# Persisted issue in database
		issue = models.Issue.objects.get(register='2015RI0000124')
		register_normalized = params['register'].replace('/', '')
		self.assertEqual(issue.register, register_normalized)
		

	def test_url_api_issues_GET(self):
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()
		issues = self.app.get('/issues/')
		data_json = issues.get_data()
		data = json.loads(data_json)
		self.assertIsInstance(data['issues'], list)
		self.assertEqual(data['issues'][0]['register'], '2015RI0000124')

	def test_url_api_issues_GET_one(self):
		pass

	"""

	def test_url_api_comments(self):
		pass

	def test_url_api_search(self):
		pass

	# SSE EVENTS TESTS
	def test_url_sse_updates(self):
		pass

	def test_url_sse_updates_comments(self):
		pass

	def test_url_sse_updates_comments_register_number(self):
		pass

	# backend Operations 
	def test_convert_links(self):
		pass

	def test_convert_hashtags(self):
		pass

	def test_convert_username(self):
		pass
	"""



if __name__ == "__main__":
	unittest.main()