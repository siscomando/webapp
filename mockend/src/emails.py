# -*- coding: utf-8 -*-
"""
Snnipet to send all emails in this app.

created by horacioibrahim at gmail dot com
created at 15/Jun/2015
"""
from flask_mail import Message
from flask import render_template
from flask.ext.babel import lazy_gettext as _
from src import app, mail, ADMINS
from src.decorators import async

@async
def async_send_mail(app, msg):
	with app.app_context():
		mail.send(msg)

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
			render_template('approved_invited.txt', 
				title=_(u"Invitation Approved"), fullname=fullname, 
				greetings=_(u"Hi"), token_url_register=token),
			render_template('approved_invited.html', 
				title=_(u"Invitation Approved"), fullname=fullname, 
				greetings=_(u"Hi"), token_url_register=token)
		)
	
def welcome_app():
	""" Triggers when the user makes the registration on app. """
	pass

def you_was_mentioned():
	""" Triggers when an user is mentioned in comments. """
	pass

def replied_from_mentioned():
	""" Triggers when the mentioned user by you reply."""
	pass