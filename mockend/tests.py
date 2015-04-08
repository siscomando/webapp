# -*- coding: utf-8 -*-
import os
import unittest
import tempfile
import json
import urllib
import random
from flask import jsonify, url_for
from sseclient import SSEClient
from tornado.testing import AsyncTestCase, AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient
#APP
from src import app, database, models


class SrcTestCase(unittest.TestCase):

	def setUp(self):
		app.config['DEBUG'] = True
		self.dbname = 'test_mockend'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		self.app = app.test_client()
		int_seed = random.randint(1, 1100)
		register = ''.join(['2015RI00001', str(int_seed)])
		self.issue_default = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'O Problema eh que a de autenticação no sistema',
			'register': register,
			'ugat': 'SUPOP',
			'ugser': 'SUPGS', 
		}		

	def tearDown(self):
		db = database.connect(self.dbname)
		db.drop_database(self.dbname)

	# REST API TESTS
	@unittest.skip("TODO: to implement this feature before release")
	def test_authentication(self):
		pass

	def test_url_api_issues_POST(self):
		""" Tests if API handling post and persists the data """
		int_seed = random.randint(1, 1100)
		register = ''.join(['2015RI00001', str(int_seed)])				
		params = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'Problema de autenticação no sistema',
			'register': register,
			'ugat': 'SUPOP',
			'ugser': 'SUPGS', 
		}
		json_data = json.dumps(params)
		json_data_length = len(json_data)
		res = self.app.post('/api/v1/issues/', data=json_data, content_type='application/json',
			content_length=json_data_length)
		# Persisted issue in database
		issue = models.Issue.objects.get(register=register)
		register_normalized = params['register'].replace('/', '')
		self.assertEqual(issue.register, register_normalized)
		

	def test_url_api_issues_GET(self):
		""" Tests if API returns a list of issues"""
		# add new issue
		register = self.issue_default['register']
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]
		issues = self.app.get('/api/v1/issues/')
		data_json = issues.get_data()
		data = json.loads(data_json)
		self.assertIsInstance(data['issues'], list)
		self.assertEqual(data['issues'][0]['register'], register)

	def test_url_api_issue_GET_one(self):
		"""Tests if API returns only one isse"""
		# add new issue
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]
		issue = self.app.get('/api/v1/issues/%s' % (issue_db.register))
		data = json.loads(issue.get_data())
		self.assertEqual(data['issue']['register'], issue_db.register)

	def test_url_api_issue_DELETE(self):
		"""Tests if API one issue is deleted """
		# add new issue
		register = self.issue_default['register']
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]
		# mock situation. The comments not can to exist
		issue = self.app.delete('/api/v1/issues/%s' % (register))
		not_found = self.app.get('/api/v1/issues/%s' % (register))
		self.assertEqual(not_found.status_code, 404)

	def test_url_api_issue_PUT(self):
		"""Tests if API can to edit one issue """
		# add new issue
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]
		change_values = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'Problema de autenticação no LDAP',
			'register': '2015RI0000124',
			'ugat': 'SUPTI',
			'ugser': 'SUPRE', 
		}
		json_change_values = json.dumps(change_values)
		json_change_values_length = len(json_change_values)
		issue = self.app.put('/api/v1/issues/', 
					data=json_change_values,
					content_type='application/json', 
					content_length=json_change_values_length)
		issue_recent = models.Issue.objects.get(register='2015RI0000124')
		issue = json.loads(issue.get_data())
		self.assertEqual(issue_recent['register'], issue['issue']['register'])
		self.assertEqual(issue['issue']['ugat'], 'SUPTI')
		self.assertEqual(issue['issue']['ugser'], 'SUPRE')
		body = u'Problema de autenticação no LDAP'
		self.assertEqual(issue_recent['body'], body)
	
	def test_url_api_comments_POST(self):
		""" Tests if API handling post and persists the comments """

		try:
			u = models.User.objects.get(email='xxx@xxx.com')
		except:
			u = models.User(email='xxx@xxx.com', password='secr3t')
			u.save()
		register = self.issue_default['register']
		params = {
			'register': register,
			'body': 'Se for autenticação o problema é novamento o LDAP!',
			'author': str(u.pk),
			'stars': 3,
			'origin': 0, 
		}
		# add new issue
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]	
		# to jsonify the params
		json_data = json.dumps(params)
		json_data_length = len(json_data)
		# to send post
		res = self.app.post('/api/v1/comments/', data=json_data, 
			content_type='application/json',
			content_length=json_data_length)
		# get modified issue
		issue = models.Issue.objects.get(register=register)
		# get comment by issue
		comments = models.Comment.objects(issue_id=issue.pk)
		# tests
		# self.assertEqual(len(comments), 1)
		self.assertEqual(issue.pk, comments[0].issue_id.pk)
		body = u'Se for autenticação o problema é novamento o LDAP!'

		print "HUMAN PRINT:", res.data
		self.assertEqual(comments[0].body, body)
		self.assertNotEqual(comments[0].shottime, -1)

	@unittest.skip("Not implemented")
	def test_url_api_comments_POST_without_Register(self):
		""" Tests if API handling post and persists the comments """
		try:
			u = models.User.objects.get(email='xxx@xxx.com')
		except:
			u = models.User(email='xxx@xxx.com', password='secr3t')
			u.save()

		params = {
			'body': 'Se for autenticação o problema é novamento o LDAP!',
			'author': str(u.pk),
		}
		# add new issue
		register = self.issue_default['register']
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]	
		# to jsonify the params
		json_data = json.dumps(params)
		json_data_length = len(json_data)
		# to send post
		res = self.app.post('/api/v1/comments/', data=json_data, 
			content_type='application/json',
			content_length=json_data_length)
		# get modified issue
		issue = models.Issue.objects.get(register=register)
		# get comment by issue
		comments = models.Comment.objects(issue_id=issue.pk)
		# tests
		# self.assertEqual(len(comments), 1)
		self.assertEqual(issue.pk, comments[0].issue_id.pk)
		#body = u'Se for autenticação o problema é novamento o LDAP!'
		self.assertEqual(comments[0].body, params['body'])		

	def test_url_api_comments_GET(self):
		""" Tests if API gets all and general comments """		
		res = self.app.get('/api/v1/comments/')
		json_data = json.loads(res.get_data())
		self.assertIsInstance(json_data['comments'], list)

	def test_url_api_comment_GET_by_ISSUE(self):
		""" Tests if API gets all from specific issue """
		# add new issue
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]
		try:
			u = models.User.objects.get(email='xxx@xxx.com')
		except:
			u = models.User(email='xxx@xxx.com', password='secr3t')
			u.save()		
		comment = models.Comment()
		comment.body = 'Atualizado novamente'
		comment.author = u		
		comment.issue_id = issue_db
		comment.save()
		res = self.app.get('/api/v1/comments/2015RI0000124/')
		json_data = json.loads(res.get_data())
		self.assertIsInstance(json_data['comments'], list)
		#self.assertEqual(len(json_data['comments']), 1)

	def test_url_api_comment_DELETE_one(self):
		""" Test if one comment is deleted """
		# TODO: only the author could to delete 
		# add new issue
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]
		try:
			u = models.User.objects.get(email='xxx@xxx.com')
		except:
			u = models.User(email='xxx@xxx.com', password='secr3t')
			u.save()			
		# add new comment	
		comment = models.Comment()
		comment.body = 'Atualizado novamente'
		comment.author = u		
		comment.issue_id = issue_db
		comment.save()
		URL = ''.join(['/api/v1/comments/', str(comment.pk), '/'])
		res = self.app.delete(URL)
		json_data = json.loads(res.get_data())
		self.assertEqual(json_data['msg'], 'Sucessful')
		self.assertEqual(res.status_code, 201)
		comments = models.Comment.objects(pk=comment.pk)
		self.assertEqual(len(comments), 0)

	def test_url_api_comment_PUT_one(self):
		"""Tests if API can to edit one comment """
		# TODO: only the author could to delete 
		# add new issue
		issue_db = models.Issue.objects.get_or_create(**self.issue_default)
		issue_db = issue_db[0]

		try:
			u = models.User.objects.get(email='xxx@xxx.com')
		except:
			u = models.User(email='xxx@xxx.com', password='secr3t')
			u.save()
		# add new comment	
		comment = models.Comment()
		comment.body = 'Atualizado novamente'
		comment.author = u		
		comment.issue_id = issue_db
		comment.save()
		# Edit fields
		params = {
			'body': 'Mudamos o body da mensagem para testar update via PUT',
			'stars': 5,
			'origin': 1, 
		}	
		json_data = json.dumps(params)		
		json_data_length = len(json_data)	
		URL = ''.join(['/api/v1/comments/', str(comment.pk), '/'])	
		res = self.app.put(URL, data=json_data, content_length=json_data_length,
			content_type='application/json')	
		# get comment persisted in database
		comment_updated = models.Comment.objects.get(pk=comment.pk)
		# test if persisted comment is equal the body updated in params
		self.assertEqual(comment_updated.body, params['body'])

	def test_url_api_search_issue(self):
		""" Tests search text. Remember that denormalization can to be needed """
		# TODO: only users from Siscomando could to search 
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()		
		results = models.Issue.objects.search_text('problema')
		self.assertIn('problema', results[0].body.lower())

	def test_url_api_search_issue_stopwords_portuguese(self):
		""" Tests if not results is raised with stopwords """
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()			
		results = models.Issue.objects.search_text('que')
		self.assertEqual(len(results), 0)

	def test_url_api_search_comment(self):
		# TODO: only users from Siscomando could to search 
		# add new issue
		try:
			u = models.User.objects.get(email='xxx@xxx.com')
		except:
			u = models.User(email='xxx@xxx.com', password='secr3t')
			u.save()		
		comment = models.Comment(body="Um comentario vago que tem as stopwords",
			author=u)
		comment.save()		
		results = models.Comment.objects.search_text('vago')
		self.assertIn('vago', results[0].body)

	def test_url_api_search_comment_stopwords_portuguese(self):
		""" Tests if not results is raised with stopwords """
		try:
			u = models.User.objects.get(email='xxx@xxx.com')
		except:
			u = models.User(email='xxx@xxx.com', password='secr3t')
			u.save()		
		comment = models.Comment(body="Um comentario vago que tem as stopwords",
			author=u)
		comment.save()		
		# .order_by('$text_score')
		results = models.Comment.objects.search_text('um')
		self.assertEqual(len(results), 0)	

class CustomsTestCase(unittest.TestCase):
	""" Tests created custom codes, adaptations, monkeys patch """
	
	def setUp(self):
		app.config['DEBUG'] = True
		app.config['TESTING'] = True
		self.dbname = 'test_mockend'
		app.config['WTF_CSRF_ENABLED'] = False
		self.app = app.test_client()
		self.issue_default = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'O Problema eh que a de autenticação no sistema',
			'register': '2015RI0000124',
			'ugat': 'SUPOP',
			'ugser': 'SUPGS', 
		}		

	def tearDown(self):
		db = database.connect(self.dbname)
		db.drop_database(self.dbname)

	def test_get_comments_to_json_modified(self):
		# add issue
		o = models.Issue()
		o.body = "Problema na rede SigaRede"
		o.title = "SICAP - SISTEMA"
		o.slug = "sicap-sistema"
		o.register = "2015RI/00000023456"
		o.ugat = "SUPOP"
		o.ugser = "SUPGS"
		o.save()
		# add user
		u = models.User()
		u.email = "horacioibrahim1@gmail.com"
		u.password = "secr3t"
		u.save()
		# add comment
		c = models.Comment()
		c.body = "Problema na conexão com a Infovia"
		c.issue_id = o
		c.author = u
		c.save()
		# get json comment
		json_data = c.to_json()
		data = json.loads(json_data)
		self.assertEqual(data['issue_id']['Issue']['register'], '2015RI00000023456')


class SSETestCase(unittest.TestCase):
	""" Tests behaviors of the SSE services

	Requires:
	* Redis server online
	* Local server online (manage.py runserver)
	  e.g:
	  		$ gunicorn -w 4 -b 127.0.0.1:9003 src:app

	* Local server listen port 9003

		print '######### IMPORTANT #########'
		print "For not to cause an 'deadlock' to use gunicorn"
		print "$ gunicorn -w 4 -b 127.0.0.1:9003 src:app"	
		print '##############################'

	"""

	def help_function_sse(self, url):
	    # Simulator Request for SSE
	    try:
	    	messages = SSEClient(url)
	    except:
	    	raise TypeError('Required developer web server not running or.' \
	    				'port not configured to 9003. See docstrings that class\n' \
	    				'$ gunicorn -w 4 -b 127.0.0.1:9003 src:app' )

	    return messages

	def setUp(self):
		app.config['DEBUG'] = True
		self.dbname = 'test_mockend'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		self.app = app.test_client()
		int_seed = random.randint(1, 1100)
		register = ''.join(['2015RI00001', str(int_seed)])
		self.email = 'sample%s@example.com' % str(int_seed)

		self.issue_default = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'The problem with authentication on system',
			'register': register,
			'ugat': 'SUPOP',
			'ugser': 'SUPGS', 
		}		

		self.sseclient = self.help_function_sse

	def tearDown(self):
		db = database.connect(self.dbname)
		db.drop_database(self.dbname)	

	def test_sse_get_issues(self):
		""" Tests if can to get data when issue is created """

		messages = self.sseclient('http://localhost:9003/api/v1/stream/issues/')
		# Issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()

		for msg in messages:
			try:
				if '_id' in msg.data:
					response = json.loads(msg.data)
					break
				else:
					raise
			except:
				pass

		self.assertEqual(response['body'], 
					'The problem with authentication on system')		

	def test_sse_get_comments(self):
	    # Issue
	    issue_db = models.Issue(**self.issue_default)
	    issue_db.save()
	    u = models.User(email=self.email, password='123');
	    u.save()
	    messages = self.sseclient('http://localhost:9003/api/v1/stream/comments/')

	    c = models.Comment(body="Um teste para comments",
	    			author=u, issue_id=issue_db)
	    c.save()
	    for msg in messages:
	    	try:
	    		if '_id' in msg.data:
	    			response = json.loads(msg.data)
	    			break
	    		else:
	    			raise
	    	except:
	    		pass

	    self.assertEqual(response['body'], 'Um teste para comments')
	    c.delete()
	    u.delete()
	    issue_db.delete()

	def test_sse_get_by_issue_oid(self):
	    # Issue
	    issue_db = models.Issue(**self.issue_default)
	    issue_db.save()
	    u = models.User(email=self.email, password='123');
	    u.save()

	    url = ''.join(['http://localhost:9003/api/v1/stream/comments/', 
	    	str(issue_db.pk), '/'])
	    # Simulator Request for SSE
	    messages = self.sseclient(url)
	    # Simulating comment added
	    c = models.Comment(body="Um teste para segundo",
	    			author=u, issue_id=issue_db)
	    c.save()
	    # Simulating browsing listen SSE Channel
	    for msg in messages:
	    	try:
	    		if '_id' in msg.data:
	    			response = json.loads(msg.data)
	    			break
	    		else:
	    			raise
	    	except:
	    		pass
	    self.assertEqual(response['body'], 'Um teste para segundo')	 
	    c.delete()
	    u.delete()
	    issue_db.delete()  
	    	

	"""
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
