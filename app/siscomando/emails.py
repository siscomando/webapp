# -*- coding: utf-8 -*-
"""
Snnipet to send all emails in this app.

created by horacioibrahim at gmail dot com
created at 15/Jun/2015
"""
from boto.ses.connection import SESConnection
from flask_mail import Message
from flask import render_template
from flask.ext.babel import lazy_gettext as _
from siscomando import app, mail
from siscomando.decorators import async

ADMINS = app.config.get('ADMINS')

@async
def async_send_mail(app, msg):
	development = app.config.get('MODE')

	with app.app_context():
		if development == 'DEVELOPMENT':
		    mail.send(msg)
		else:
			ses = SESConnection(
				aws_access_key_id=app.config.get('AWS_ACCESS_KEY_ID'), 
				aws_secret_access_key=app.config.get('AWS_SECRET_ACCESS_KEY'))			
			ses.send_email(msg.sender, msg.subject, msg.body, msg.recipients, 
				html_body=msg.html)

def default_send_mail(subject, sender, recipients, body_text, body_html=None):
	""" To send message by flask-mail lib using threading """
	if type(recipients) is not list:
		recipients = [recipients,]
	recipients = recipients
	msg = Message()
	msg.subject = subject
	msg.sender = sender
	msg.recipients = recipients
	msg.body = body_text
	msg.html = body_html
	async_send_mail(app, msg)

def request_invited(fullname, email):
	""" When the user requests an invite a return message is sent for it. """

	default_send_mail(
			_(u"We've received your invitation request."),
			ADMINS[0], 
			email,
			render_template('mails/request_invited.txt', 
				title=_(u"Invitation Request"), fullname=fullname, greetings=_(u"Hi")),
			render_template('mails/request_invited.html', 
				title=_(u"Invitation Request"), fullname=fullname, greetings=_(u"Hi"))
		)

def approved_invited(fullname, email, token):
	""" Triggers when the admin to approve an user to access the app. """
	default_send_mail(
			_(u"You invitation was approved!"),
			ADMINS[0], 
			email,
			render_template('mails/approved_invited.txt', 
				title=_(u"Invitation Approved"), fullname=fullname, 
				greetings=_(u"Hi"), token_url_register=token),
			render_template('mails/approved_invited.html', 
				title=_(u"Invitation Approved"), fullname=fullname, 
				greetings=_(u"Hi"), token_url_register=token)
		)
	
def welcome_app():
	""" Triggers when the user makes the registration on app. """
	pass

def you_was_mentioned(user_said, mentioned_name, mentioned_email, url_comment):
	""" Triggers when an user is mentioned in comments. """
	title = _(u"{} mentioned you in a comment".format(user_said))
	
	default_send_mail(
			title,
			ADMINS[0], 
			mentioned_email,
			render_template('mails/you_was_mentioned.txt', 
				title=title, mentioned=mentioned_name, 
				greetings=_(u"Hi"), url_comment=url_comment),
			render_template('mails/you_was_mentioned.html', 
				title=title, fullname=mentioned_name, 
				greetings=_(u"Hi"), url_comment=url_comment)
		)

def replied_from_mentioned():
	""" Triggers when the mentioned user by you reply."""
	pass