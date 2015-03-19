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
def get_issues():
	issues = models.Issue.objects()
	return jsonify({'issues': issues}), 201

@app.route('/issues/<string:register>', methods=['GET'])
def get_issue(register):
	issue = models.Issue.objects.get_or_404(register=register)
	return jsonify({'issue': issue})	

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
	""" Edits an issue
	"""
	if not request.json or 'register' not in request.json:
		abort(404)

	json_data = request.get_json()
	issue = models.Issue.objects.get(register=json_data['register'])
	issue.title = json_data.get('title', None)
	issue.slug = json_data.get('slug', None)
	issue.body = json_data.get('body', None)
	issue.classifier = json_data.get('classifier', None)
	issue.ugat = json_data.get('ugat', None)
	issue.ugser = json_data.get('ugser', None)
	issue.deadline = json_data.get('deadline', None)
	issue.save()

	return jsonify({'issue': issue}), 201

@app.route('/issues/<string:register>', methods=['DELETE'])
def del_issues(register):
	issue = models.Issue.objects.get_or_404(register=register)
	issue.delete()
	return jsonify({'msg': 'Sucessful'}), 201


# Comments
@app.route('/comments/', methods=['POST'])
def set_comments():
	""" Creates a comment in database

	JSON scope:
		@param register is required

	"""
	if not request.json or 'register' not in request.json:
		abort(400)

	json_data = request.get_json()
	register = json_data['register']
	# the place (issue) where will save the comments
	issue = models.Issue.objects.get_or_404(register=register)
	# create comment
	body = json_data.get('body')
	author = json_data.get('author')
	stars = json_data.get('stars', 0)
	origin = json_data.get('origin')
	comment = models.Comment(issue_id=issue, body=body, author=author, stars=stars, 
    				origin=origin)
	comment.save()
	# add comment in issue

	return jsonify({'comment': comment}), 201

@app.route('/comments/', methods=['GET'])	
def get_comments():
	comments = models.Comment.objects()
	return jsonify({'comments': comments})

@app.route('/comments/<string:register>/', methods=['GET'])	
def get_comments_from_register(register):
	issue = models.Issue.objects.get_or_404(register=register)
	comments = models.Comment.objects(issue_id=issue.pk)
	return jsonify({'comments': comments}), 201

@app.route('/comments/<string:objectid>/', methods=['DELETE'])	
def del_comments(objectid):
	comment = models.Comment.objects.get_or_404(pk=objectid)
	comment.delete()
	return jsonify({'msg': 'Sucessful'}), 201

@app.route('/comments/<string:objectid>/', methods=['PUT'])	
def edit_comments(objectid):
	comment = models.Comment.objects.get_or_404(pk=objectid)
	
	if not request.json:
		abort(400)
	# json loads
	json_data = request.get_json()
	# fields allowed (not can edit author, issue_id, created_at)
	comment.body = json_data.get('body')
	comment.stars = json_data.get('stars')
	comment.origin = json_data.get('origin')
	comment_edited = comment.save()

	return jsonify({'comment': comment_edited}), 201	

