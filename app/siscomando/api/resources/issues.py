from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from siscomando import models

class BaseIssues(restful.Resource):

    issues_fields = {
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


class Issues(BaseIssues):
	
    @marshal_with(BaseIssues.issues_fields)
    def get(self):
        issues = models.Issue.objects()
        return issues



