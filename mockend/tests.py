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
			'body': 'O Problema eh que a de autenticação no sistema',
			'register': '2015RI/0000124',
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
		params = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'Problema de autenticação no sistema',
			'register': '2015RI/0000124',
			'ugat': 'SUPOP',
			'ugser': 'SUPGS', 
		}
		json_data = json.dumps(params)
		json_data_length = len(json_data)
		res = self.app.post('/issues/', data=json_data, content_type='application/json',
			content_length=json_data_length)
		# Persisted issue in database
		issue = models.Issue.objects.get(register='2015RI0000124')
		register_normalized = params['register'].replace('/', '')
		self.assertEqual(issue.register, register_normalized)
		

	def test_url_api_issues_GET(self):
		""" Tests if API returns a list of issues"""
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()
		issues = self.app.get('/issues/')
		data_json = issues.get_data()
		data = json.loads(data_json)
		self.assertIsInstance(data['issues'], list)
		self.assertEqual(data['issues'][0]['register'], '2015RI0000124')

	def test_url_api_issue_GET_one(self):
		"""Tests if API returns only one isse"""
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()
		issue = self.app.get('/issues/2015RI0000124')
		data = json.loads(issue.get_data())
		self.assertEqual(data['issue']['register'], '2015RI0000124')

	def test_url_api_issue_DELETE(self):
		"""Tests if API one issue is deleted """
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()	
		issue = self.app.delete('/issues/2015RI0000124')
		not_found = self.app.get('/issues/2015RI0000124')
		self.assertEqual(not_found.status_code, 404)

	def test_url_api_issue_PUT(self):
		"""Tests if API can to edit one issue """
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()	
		change_values = {
			'title': 'ALM - GERENCIAMENTO',
			'body': 'Problema de autenticação no LDAP',
			'register': '2015RI0000124',
			'ugat': 'SUPTI',
			'ugser': 'SUPRE', 
		}
		json_change_values = json.dumps(change_values)
		json_change_values_length = len(json_change_values)
		issue = self.app.put('/issues/', 
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
		params = {
			'register': '2015RI0000124',
			'body': 'Se for autenticação o problema é novamento o LDAP!',
			'author': 'horacioibrahim',
			'stars': 3,
			'origin': 0, 
		}
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()			
		json_data = json.dumps(params)
		json_data_length = len(json_data)
		res = self.app.post('/comments/', data=json_data, content_type='application/json',
			content_length=json_data_length)
		issue = models.Issue.objects.get(register='2015RI0000124')
		comments = models.Comment.objects(issue_id=issue.pk)
		self.assertEqual(len(comments), 1)
		self.assertEqual(issue.pk, comments[0].issue_id.pk)
		body = u'Se for autenticação o problema é novamento o LDAP!'
		self.assertEqual(comments[0].body, body)

	def test_url_api_comments_GET(self):
		""" Tests if API gets all and general comments """		
		res = self.app.get('/comments/')
		json_data = json.loads(res.get_data())
		self.assertIsInstance(json_data['comments'], list)

	def test_url_api_comment_GET_by_ISSUE(self):
		""" Tests if API gets all from specific issue """
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()	
		comment = models.Comment()
		comment.body = 'Atualizado novamente'
		comment.author = 'maresiadasilva'		
		comment.issue_id = issue_db
		comment.save()
		res = self.app.get('/comments/2015RI0000124/')
		json_data = json.loads(res.get_data())
		self.assertIsInstance(json_data['comments'], list)
		self.assertEqual(len(json_data['comments']), 1)

	def test_url_api_comment_DELETE_one(self):
		""" Test if one comment is deleted """
		# TODO: only the author could to delete 
		# add new issue
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()
		# add new comment	
		comment = models.Comment()
		comment.body = 'Atualizado novamente'
		comment.author = 'maresiadasilva'		
		comment.issue_id = issue_db
		comment.save()
		URL = ''.join(['/comments/', str(comment.pk), '/'])
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
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()
		# add new comment	
		comment = models.Comment()
		comment.body = 'Atualizado novamente'
		comment.author = 'maresiadasilva'		
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
		URL = ''.join(['/comments/', str(comment.pk), '/'])	
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
		self.assertEqual(len(results), 1)

	def test_url_api_search_issue_stopwords_portuguese(self):
		""" Tests if not results is raised with stopwords """
		issue_db = models.Issue(**self.issue_default)
		issue_db.save()			
		results = models.Issue.objects.search_text('que')
		self.assertEqual(len(results), 0)

	def test_url_api_search_comment(self):
		# TODO: only users from Siscomando could to search 
		# add new issue
		comment = models.Comment(body="Um comentario vago que tem as stopwords",
			author="horacioibrahim")
		comment.save()		
		results = models.Comment.objects.search_text('vago')
		self.assertEqual(len(results), 1)

	def test_url_api_search_comment_stopwords_portuguese(self):
		""" Tests if not results is raised with stopwords """
		comment = models.Comment(body="Um comentario vago que tem as stopwords",
			author="horacioibrahim")
		comment.save()		
		# .order_by('$text_score')
		results = models.Comment.objects.search_text('um')
		self.assertEqual(len(results), 0)		

	# SSE EVENTS TESTS
	"""
	def test_url_sse_updates(self):
		pass

	def test_url_sse_updates_comments(self):
		pass

	def test_url_sse_updates_comments_register_number(self):
		pass
	"""

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