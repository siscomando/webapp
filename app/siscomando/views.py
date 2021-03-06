# -*- coding: utf-8 -*-
import logging, json, re, base64, datetime
from flask.views import View
from flask import (jsonify, request, make_response, abort, Response, flash,
					render_template, flash, url_for, redirect, session, g)
from flask.ext.login import login_required, current_user, login_user, logout_user
from flask.ext.babel import lazy_gettext as _
# APP
from siscomando import app, red, models, login_manager, utils
from siscomando.utils import generate_token

#
# Setup flask-login
#
@login_manager.user_loader
def load_user(id):
	"""Because pk is unique we can to use filter. It will return the user or
	None if user not exists."""
	u = models.User.objects.filter(pk=id).first()
	return u

@app.before_request
def before_request():
    g.user = current_user

# APP
@app.errorhandler(404)
def not_found_error(error):
	output = {'message': 'Not Found'}
	return make_response(jsonify(output), 404)

@app.errorhandler(500)
def internal_error(error):
	output = {"message": 'Internal error'}
	return make_response(jsonify(output), 500)

#
# Static routes
#
@app.route('/')
def index():

	if current_user.is_authenticated():
		return redirect(url_for('application'))

	return render_template('home.html')

@app.route('/logout/')
@login_required
def logout():
	u = current_user
	u.status_online = False
	logout_user()
	return redirect(url_for('index'))

@app.route('/login/', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':
		email = request.form['identifier']
		password = request.form['password']
		registered_user = models.User.objects.filter(email=email).first()

		if registered_user is None or \
			registered_user.check_password(password) is not True:
			flash('Username or Password is invalid', 'error') # TODO
			return redirect(url_for('login'))

		login_user(registered_user, remember=True)
		flash('Logged in successfully')
		return redirect(request.args.get('next') or url_for('application'))

	# return jsonify({'msg': 'Sucessful'}), 201
	return render_template('login.html')

@app.route('/login_api/', methods=['POST'])
def login_api():

	if not request.json:
		abort(400)

	if request.method == 'POST':
		data = request.get_json()
		email = data['identifier']
		password = data['password']
		registered_user = models.User.objects.filter(email=email).first()

		if registered_user is None or \
			registered_user.check_password(password) is not True:
			return  jsonify({
					'message': {
						'type': 'error',
						'status': 'Username or Password is invalid',
						'_links': url_for('login_api')
					}
			}), 401

		login_user(registered_user, remember=True)
		token = generate_token(registered_user.email)
		registered_user.token = token
		registered_user.save()

		return  jsonify({
				'message': {
					'type': 'info',
					'status': 'Logged in successfully',
					'_links': url_for('application'),
					'token': token,
					'user': str(registered_user.pk),
					'created_at': str(datetime.datetime.now())
				}
		}), 200

@app.route('/register/<string:token>/', methods=['GET'])
def register(token):
	# TODO: TESTAR LOGIN REDIRECT
	# TODO: RESETAR SENHA
    if request.method == 'GET':
    	invited = models.Invite.objects.get_or_404(pk=token)
    	if invited.is_approved == True and invited.used == False:
    		name = invited.name.split()[0].capitalize()
        	return render_template('register.html', greetings=_(u'Hi'),
        		name=name, invite=invited)
        else:
        	return render_template('not_approved_invited.html', greetings=_(u'Hi'),)

@app.route('/register/', methods=['POST'])
def register_new():
	invite_pk = request.form.get('invite')
	invited = models.Invite.objects.get_or_404(pk=invite_pk)
	user = models.User()
	user.email =  invited.email
	user.password = request.form.get('password', None)

	if user.email is None or user.password is None:
		flash('The typed User or Password is invalid', 'error')

	try:
		user.save(to_change_pass=True)
		flash('Account created with successfully!')
		return redirect(url_for('login'))
	except:
		flash('User already exists. Try login!', 'error')
		return redirect(url_for('login'))

	flash('User successfully registered') # TODO name already exists
	return redirect(url_for('index'))

@app.route('/settings/', methods=['GET'])
def settings():
 	''' Profile user '''

 	return render_template('settings.html')

@app.route('/request_invite/', methods=['POST'])
def request_invite():
 	name = request.form['name']
 	email = request.form['email']
 	invite = models.Invite()
 	invite.name = name
 	invite.email = email

 	#try:
 	invite.save()
 	#except:
 	#	#erro nome, email estao em vazios
 	#	return render_template('request_invite_failed.html')

 	return render_template('request_invite_successful.html')


@app.route('/app/', methods=['GET'])
@login_required
def application():

	if current_user.is_authenticated():
		return render_template('app.html')
	else:
		return login()

@app.route('/hashtag/<string:hash>/', methods=['GET'])
def get_hashtags(hash):
	# get messages by hashtags and get hashtags
	pass

# API REQUESTS
@app.route('/api/v1/stars/<string:target>/', methods=['POST'])
@login_required
def set_stars(target):
    """ Set valuation of the target
    """
    if not request.json:
    	abort(400)

    if target == "comments":
    	json_data = request.get_json()
    	pk = json_data['pk']
    	score = json_data['score']
    	comment = models.Comment.objects.get_or_404(pk=pk)
    	star = models.ScoreStars()
    	star.score = score
    	star.voter = models.User.objects.get(pk=current_user.pk)
    	comment.stars.append(star)
    	comment.save()
    	data = json.loads(comment.to_json())
    	data = {'comment': data}
        return jsonify(data), 201

	return jsonify({'Not implemented target'}), 401

@app.route('/api/v1/search/', methods=['POST'])
@login_required
def search():
	# TODO: FTS - full text search

	if not request.json:
		abort(400)

	json_data = request.get_json()
	term = json_data['term']
	register = json_data.get('register', None)

	if term is None or term == '':
		return get_comments() # workaround for presentation

	rex = re.compile('(^in:[ ]?)(.*)')
	matched = rex.match(term)
	# If the `term` is initiate with expression `in:` and the register number
	# was sent to search inside Issue.
	if matched and register:
		term = matched.groups()[1]
		issue = models.Issue.objects.get_or_404(register=register)
		comments = models.Comment.objects(body__icontains=term, issue_id=issue)
	else:
		comments = models.Comment.objects(body__icontains=term)

	json_data = json.loads(comments.to_json())
	data = {'comments': json_data}
	return jsonify(data), 200

@app.route('/api/v1/users/<string:expr>/<string:limit>/')
@app.route('/api/v1/users/<string:expr>/')
@login_required
def get_users(expr, limit=None):
	""" Gets users from string of the mentions typed by users."""
	if expr.startswith('@'):
		expr = expr[1:]

	if limit is None:
		limit = 100

	users = models.User.objects(shortname__icontains=expr).limit(int(limit)) # TODO: to deploy FTS
	json_data = json.loads(users.to_json())
	data = {'Users': json_data}
	return jsonify(data), 200

@app.route('/api/v1/issues/', methods=['GET'])
@login_required
def get_issues():
	issues = models.Issue.objects()
	return jsonify({'issues': issues}), 200

@app.route('/api/v1/issues/<string:register>/', methods=['GET'])
@login_required
def get_issue(register):
	issue = models.Issue.objects.get_or_404(register=register)
	return jsonify({'issue': issue})

@app.route('/api/v1/issues/', methods=['POST'])
@login_required
def set_issues():
	""" Persists the JSON from request in database

	TODO:
	 - needs control access at resource
	 - new fields
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

	TODO:
	 - needs control access at resource
	 - new fields
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

@app.route('/api/v1/issues/<string:register>/', methods=['DELETE'])
@login_required
def del_issues(register):
	"""
	TODO: It needs control access
	"""
	issue = models.Issue.objects.get_or_404(register=register)
	issue.delete()
	return jsonify({'msg': 'Sucessful'}), 201


# Comments
@app.route('/api/v1/comments/', methods=['POST'])
@login_required
def set_comments():
	""" Creates a comment in database

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

	if str(current_user.pk) != str(author):
		abort(401) # Secure this view. Validation origin user.

	# the place (issue) where will save the comments
	if register:
		issue = models.Issue.objects.get_or_404(register=register)
	else:
		issue = None

	# TODO: Check if author is the same users logged !!!
	comment = models.Comment(issue_id=issue, body=body, author=author,
    				origin=origin)

	try:
		comment.save()
	except:
		data = {'errors': "Selecione um chamado no menu ou escreva colocando " \
				"uma #hashtag para definir o #Assunto."}
		return jsonify(data), 403

	json_data = json.loads(comment.to_json())
	data = {'comments': json_data}

	return jsonify(data), 201

@app.route('/api/v1/comments/', methods=['GET'])
@login_required
def get_comments():
	start = 0
	end = 25 # the comments retunes if not passed arg page
	page = request.args.get('page', 1)
	if page:
		page = page if isinstance(page, int) else int(page)
		page = page if page > 0 else 1
		start = (end * (page - 1))
		end = end * page
	comments = models.Comment.objects[start:end] # plus closed last
	json_data = json.loads(comments.to_json(current_user=current_user))
	data = {'comments': json_data}
	return jsonify(data), 200

@app.route('/api/v1/comments/<string:register>/', methods=['GET'])
@login_required
def get_comments_from_register(register):
	page = request.args.get('page', None)

	# Workaround to return something but not comments. Because all comments
	# is returned in the first request. This view not needs pagination on now.
	if page:
		return jsonify({'message': u'All messages already returned.'}), 200

	issue = models.Issue.objects.get_or_404(register=register)
	comments = models.Comment.objects(issue_id=issue.pk)
	json_data = json.loads(comments.to_json())
	data = {'comments': json_data}
	return jsonify(data), 200

@app.route('/api/v1/comments/<string:oid>/', methods=['DELETE'])
@login_required
def del_comments(oid):
	comment = models.Comment.objects.get_or_404(pk=oid)
	# Only user that is author can delete it
	if str(comment.author.pk) != str(current_user.pk):
		abort(401)

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
	# fields allowed (the field author, issue_id, created_at is not editable)
	# and only the user that is author can edit it
	if str(comment.author.pk) != str(current_user.pk):
		abort(401)

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
