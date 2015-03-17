# -*- coding: utf-8 -*-
from flask.views import View
from flask import jsonify, request, make_response, abort
#APP
from src import app
from src import models


# APP
@app.errorhandler(404)
def not_found_error(error):
	output = {'error': 'Not found'}
	return make_response(jsonify(output), 404)

@app.errorhandler(500)
def internal_error(error):
	output = {"error": 'Internal error'}
	return make_response(jsonify(output), 500)

# API REQUESTS 
@app.route('/')
@app.route('/index')
def index():
	return "Passed by here"

@app.route('/issues/', methods=['GET'])
def get_issues(issue_id=None):
	issues = models.Issue.objects()
	return jsonify({'issues': issues})

@app.route('/issues/', methods=['POST'])
def set_issues():
	""" Persists the JSON from request in database
	"""
	if not request.json:
		abort(400)

	json_data = request.get_json()
	issue = models.Issue()
	issue.title = json_data['title']
	issue.body = json_data['body']
	issue.register = json_data['register']
	issue.ugat = json_data['ugat']
	issue.ugser = json_data['ugser']
	new_issue = issue.save()
	return jsonify({'issue': new_issue}), 201

@app.route('/issues/', methods=['PUT'])
def edit_issues():
	pass

@app.route('/issues/', methods=['DELETE'])
def del_issues():
	pass