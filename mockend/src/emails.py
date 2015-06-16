# -*- coding: utf-8 -*-
"""
Snnipet to send all emails in this app.

created by horacioibrahim at gmail dot com
created at 15/Jun/2015
"""

from flask_mail import Message
from flask import render_template
from src import mail, ADMINS

def default_send_mail(subject, sender, recipients, body_text, body_html=None):
	""" To send message by flask-mail lib """
	if type(recipients) is not list:
		recipients = [recipients,]
	recipients = recipients
	msg = Message()
	msg.subject = subject
	msg.sender = sender
	msg.recipients = recipients
	msg.body = body_text
	msg.html = body_html
	mail.send(msg) # TODO: Gevent to async tasks 

def request_invited(fullname, email):
	""" When the user requests an invite a return message is sent for it. """
	default_send_mail(
			_(u"We've received your invitation request."),
			ADMINS[0], 
			email,
			render_template('request_invited.txt', fullname=fullname),
			render_template('request_invited.html', fullname=fullname)
		)

def approved_invited():
	""" Triggers when the admin to approve an user to access the app. """
	pass

def welcome_app():
	""" Triggers when the user makes the registration on app. """
	pass

def you_was_mentioned():
	""" Triggers when an user is mentioned in comments. """
	pass

def replied_from_mentioned():
	""" Triggers when the mentioned user by you reply."""
	pass