# settings for RESTful API
# 
from api.schemas import users_schema, issues_schema
DEBUG = True

# Database setup
MONGO_HOST = "localhost"
MONGO_POST = "27017"
# MONGO_DBNAME is temporally added hard but place it app's global settings.
MONGO_DBNAME = "dev_scdb" 

# Versioning 
URL_PREFIX = "api"
API_VERSION = "v2"

# Feature to expand embedded documents from reference fields
QUERY_EMBEDDED = "expanded" # Changed from embedded to expanded

# Scope from models. Custom properties.
DATE_CREATED = "created_at"
LAST_UPDATED = "updated_at"

DOMAIN = {}

DOMAIN_EVE = {
	'users': {
		'url': 'users',
		'datasource': {
			'source': 'user',
			'projection': {'password': 0}
		},
		'cache_control': '', # account cache is not needs. 
		'cache_expires': 0,
		#'allowed_roles': ['superusers'],
		#'allowed_read_roles': ['users'],
		#'allowed_write_roles': ['superusers'],
		#'allowed_item_write_roles': ['superusers'],
		#'auth_field': 'pk',
		#'item_methods': ['PATCH', 'DELETE'],
		# 'resource_methods': ['GET', 'POST'],
		#'soft_delete': True, # not working
		# 'schema': users_schema, EVEMongoengine
	},
	'issues': {
		'url': 'issues',
		'datasource': {
			'source': 'issue'
		},
		'allowed_roles': ['users'],
		#'allowrd_write_roles' : ['admins'],
		#'url': '/issue/',
		# by default is ObjectId. We also enable an additional read-only entry
		# point. This ways consumers can also perform GET requests at
		# '/issue/<register>'.
		# First to define SCHEME
		#'additional_lookup': {
		#	'field': 'register',
		#	'url': 'regex("[\w]+")'
		#},
		'resource_methods': ['GET', 'POST'], # TODO: updates
		# 'schema': issues_schema,
	},
	'comments': {
		'url': 'comments',
		'datasource': {
			'source': 'comment'
		},
		'auth_field': 'author', # Only owner can to read and update actions. 
	}
}

# SOFT_DELETE = True # NOT WORKING see more: http://python-eve.org/features.html#soft-delete
XML = False
IF_MATCH = False # CAUTION: temporally disabled. This keeps versions correclty updated.
# PUBLIC_METHODS = ['GET'] # This override auth_field behavior 
# PUBLIC_ITEM_METHODS = ['GET'] # This override auth_field behavior 
# ALLOWED_ROLES = ['users'] # minimal role required.