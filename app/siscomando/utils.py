# -*- coding: utf-8 -*-

"""
 Utils.py
"""
import datetime
import base64
import jwt
from siscomando import app


def generate_token(user_id):
    secret_key = app.config.get("SECRET_KEY")
    payload = {
        'sub': str(user_id),
        'iat': datetime.datetime.now()
    }
    encoded = jwt.encode(payload, secret_key, algorithm='HS256')
    return base64.b64encode(encoded + ':')
