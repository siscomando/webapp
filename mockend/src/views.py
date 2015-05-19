# -*- coding: utf-8 -*-
from flask.views import View
from flask import jsonify, request, make_response, abort, Response, flash
from flask import render_template, flash, url_for, redirect, session, g
from flask.ext.login import login_required, current_user, login_user, logout_user
import logging
import json
# APP
from src import app, red, models, login_manager

# Setup flask-login
@login_manager.user_loader
def load_user(id):
    return models.User.objects.get(pk=id)

@app.before_request
def before_request():
    g.user = current_user    

# APP
@app.errorhandler(404)
def not_found_error(error):
	output = {'error': 'Not found'}
	return make_response(jsonify(output), 404)

@app.errorhandler(500)
def internal_error(error):
	output = {"error": 'Internal error'}
	return make_response(jsonify(output), 500)

@app.route('/mocklogin', methods=['GET'])
def mocklogin():
	users = models.User.objects()
	return render_template('mocklogin.html', users=users)

@app.route('/')
@app.route('/index')
def index():

	# if user.is_authenticated():
		# redirect to home
	# else:
		# to login or register user

	return redirect(url_for('login')) # TODO: landingpage

@app.route('/logout')
@login_required
def logout():
	u = current_user
	u.status_online = False
	logout_user()
	return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	# TODO: FAZER LOGIN
	# TODO: REDIRECT HOME
	if request.method == 'POST':
		email = request.form['identifier']
		password = request.form['password']
		registered_user = models.User.objects.filter(email=email, 
				password=password).first()
		if registered_user is None:
			flash('Username or Password is invalid', 'error') # TODO
			return redirect(url_for('login'))

		login_user(registered_user, remember=True)
		flash('Logged in successfully')
		return redirect(request.args.get('next') or url_for('application'))
	
	# return jsonify({'msg': 'Sucessful'}), 201
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	# TODO: TESTAR LOGIN REDIRECT
	# TODO: RESETAR SENHA
    if request.method == 'GET':
        return render_template('register.html')

    user = models.User()
    user.email =  request.form.get('identifier', None)
    user.password = request.form.get('password', None)

    if user.email is None or user.password is None:
    	flash('The typed User or Password is invalid', 'error')

    try:
    	user.save()
    except:
    	flash('User or password is invalid or already exists', 'error')

    flash('User successfully registered') # TODO name already exists
    return redirect(url_for('login'))
    
@app.route('/app', methods=['GET'])
@login_required
def application():

	#if user.is_authenticated():
	#	return render_template('app.html')
	# else:
	#	return login()
	return render_template('app.html')

# API REQUESTS 
@app.route('/api/v1/users/<string:expr>')
@login_required
def get_users(expr):
	""" Gets users from string of the mentions typed by users."""
	if expr.startswith('@'):
		expr = expr[1:]

	users = models.User.objects(shortname__icontains=expr) # TODO: to deploy FTS
	json_data = json.loads(users.to_json())
	data = {'Users': json_data}
	return jsonify(data), 201

@app.route('/api/v1/issues/', methods=['GET'])
@login_required
def get_issues():
	issues = models.Issue.objects()
	return jsonify({'issues': issues}), 201

@app.route('/api/v1/issues/<string:register>', methods=['GET'])
@login_required
def get_issue(register):
	issue = models.Issue.objects.get_or_404(register=register)
	return jsonify({'issue': issue})	

@app.route('/api/v1/issues/', methods=['POST'])
@login_required
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

@app.route('/api/v1/issues/', methods=['PUT'])
@login_required
def edit_issues():
	""" Edits an issue

	TODO: needs control access at resource
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

@app.route('/api/v1/issues/<string:register>', methods=['DELETE'])
@login_required
def del_issues(register):
	issue = models.Issue.objects.get_or_404(register=register)
	issue.delete()
	return jsonify({'msg': 'Sucessful'}), 201


# Comments
@app.route('/api/v1/comments/', methods=['POST'])
@login_required
def set_comments():
	""" Creates a comment in database

	JSON scope:
		@param register is required

	"""
	if not request.json:
		abort(400)

	json_data = request.get_json()
	# logging.info(json_data)
	register = json_data.get('register', None)
	# create comment
	body = json_data.get('body')
	author = json_data.get('author')
	stars = json_data.get('stars', 0)
	origin = json_data.get('origin')
	# the place (issue) where will save the comments
	if register:
		issue = models.Issue.objects.get_or_404(register=register)
	else:
		abort(400) # not issue found
		issue = None

	comment = models.Comment(issue_id=issue, body=body, author=author, stars=stars, 
    				origin=origin)
	comment.save()
	json_data = json.loads(comment.to_json())
	data = {'comments': json_data}
	
	return jsonify(data), 201

@app.route('/api/v1/comments/', methods=['GET'])
@login_required	
def get_comments():
	comments = models.Comment.objects()
	json_data = json.loads(comments.to_json())
	data = {'comments': json_data}
	return jsonify(data), 201

@app.route('/api/v1/comments/<string:register>/', methods=['GET'])
@login_required	
def get_comments_from_register(register):
	issue = models.Issue.objects.get_or_404(register=register)
	comments = models.Comment.objects(issue_id=issue.pk)
	json_data = json.loads(comments.to_json())
	data = {'comments': json_data}
	return jsonify(data), 201

@app.route('/api/v1/comments/<string:oid>/', methods=['DELETE'])
@login_required	
def del_comments(oid):
	comment = models.Comment.objects.get_or_404(pk=oid)
	comment.delete()
	return jsonify({'msg': 'Sucessful'}), 201

@app.route('/api/v1/comments/<string:oid>/', methods=['PUT'])
@login_required	
def edit_comments(oid):
	comment = models.Comment.objects.get_or_404(pk=oid)
	
	if not request.json:
		abort(400)
	# json loads
	json_data = request.get_json()
	# fields allowed (not can edit author, issue_id, created_at)
	comment.body = json_data.get('body')
	comment.stars = json_data.get('stars')
	comment.origin = json_data.get('origin')
	comment.save()

	json_data = json.loads(comment.to_json())
	data = {'comment': json_data}
	return jsonify(data), 201	

def event_stream(channel):
	pubsub = red.pubsub()
	pubsub.subscribe(channel)
	# Set client side auto reconnect timeout, ms.
	yield 'retry: 15000\n\n'
	for message in pubsub.listen():
		yield 'data: %s\n\n' % message['data']

@app.route('/api/v1/stream/comments/', methods=['GET'])
@login_required
def stream_comments():
	""" Gets new issues and fire it in the Redis. 

	Specifically in Siscomando this can to be used in Navbar (sc-navbar)
	""" 
	return Response(event_stream('comments'), mimetype='text/event-stream', 
		headers=[('cache_control', 'no-cache')])

@app.route('/api/v1/stream/comments/<string:issueoid>/', methods=['GET'])
@login_required
def stream_comments_by_issue(issueoid):
	""" Gets new comments based in Issue Object ID and fire it in the Redis. 
	""" 
	channel = ''.join(['comments', issueoid])
	return Response(event_stream(channel), mimetype='text/event-stream', 
		headers=[('cache_control', 'no-cache')])	

@app.route('/api/v1/stream/issues/')
@login_required
def stream_by_issues():
	""" Gets new issues

	TODO: Only authenticated user could to access this API
	"""
	return Response(event_stream('issues'), mimetype='text/event-stream', 
		headers=[('cache_control', 'no-cache')])	

# @app.route('/api/v1/stream/issues/<string:oid>')




