from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from siscomando import models


class Issues(restful.Resource):
	
    _fields = {
        'pk': fields.String,
        'register': fields.String,
        'title': fields.String,
        'body': fields.String,
        'classifier': fields.Integer,
        'ugat': fields.String,
        'ugser': fields.String,
        'deadline': fields.Integer,
        'closed': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'register_orig': fields.String
    }

    @marshal_with(_fields)
    def get(self):
        issues = models.Issue.objects()
        return issues

    def get_issue(self, register, filters=None):
        pass

    def post(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


