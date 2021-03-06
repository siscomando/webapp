import datetime
import json
import md5
import re
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import signals, CASCADE, DENY
from flask.ext.mongoengine import BaseQuerySet
from bson import json_util
from cerberus import Validator
# APP
from siscomando import database as db
from siscomando import red, emails, login_manager

# Hints:
# We can denormalization. See more 1-2-3 by starting here:
# http://blog.mongodb.org/post/87200945828/6-rules-of-thumb-for-mongodb-schema-design-part-1
#

# SSE Events support
def publish_in_redis(channel, data):
    return red.publish(channel, data)

class CustomQuerySet(BaseQuerySet):
    def to_json(self, current_user=None):
        return "[%s]" % (','.join([doc.to_json(current_user=current_user) for doc in self]))

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField()
    location = db.StringField(max_length=25)
    shortname = db.StringField(max_length=80)
    username = db.StringField(max_length=80)
    avatar = db.StringField() # URL
    status_online = db.BooleanField(default=True)
    md5_email = db.StringField()
    token = db.StringField(unique=True)
    roles = db.ListField(db.StringField()) # users, admins, superusers
    owner = db.ReferenceField('User')


    meta = {'queryset_class': CustomQuerySet}

    # Deprecated after implemented Eve.
    # Eve is bare with MongoDB him have projection by resources. This is allows
    # to filter (or exclude) fields.
    # E.g.: projection: {'password': 0}
    def to_json(self, current_user=None):
        data = self.to_mongo()
        data['password'] = None # wrapper to omit password. It's not needs with Eve.
        return json_util.dumps(data)

    # This methods are useful for HTML rendering or view handling. When
    # implemented the Eve API all requests will to need authentication.
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.pk)

    def __repr__(self):
        return '<User %r>' % (self.email)

    def validate_email(self):
        schema = {'email': {'type':'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]+$'}}
        fragment = {'email': self.email}
        v = Validator()

        if v.validate(fragment, schema):
            self.set_shortname()
        else:
            raise TypeError('Mail address malformed')

    # This methods (set_shortname, set_password and check_password) will be
    # hooks in the Eve API.
    def set_shortname(self):
        self.shortname = self.email.split('@')[0]
        self.username = self.shortname

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self, *args, **kwargs):
        # to_change_pass is argument that works as workaround to set
        # new password intentionally by user. Default is False.
        to_change_pass = kwargs.get('to_change_pass', False)
        self.validate_email()
        self.set_shortname()
        if to_change_pass:
            self.set_password(self.password)
        self.md5_email = md5.md5(self.email).hexdigest()
        super(User, self).save(*args, **kwargs)


class Issue(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField()
    title = db.StringField(max_length=150, required=True)
    slug = db.StringField(max_length=255, required=False) # TODO slugfy
    body = db.StringField(required=True)
    register = db.StringField(max_length=50, required=True, unique=True)
    register_orig = db.StringField(max_length=51)
    classifier = db.IntField(default=0) # high, highest ...
    ugat = db.StringField(max_length=12, required=True)
    ugser = db.StringField(max_length=12, required=True)
    deadline = db.IntField(default=120)
    closed = db.BooleanField(default=False)
    author = db.ReferenceField('User', required=True)


    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if ('created' in kwargs and kwargs['created']) or document.closed == True:
            publish_in_redis('issues', document.to_json())

    def get_absolute_url(self):
        return url_for('issue', kwargs={'slug': self.slug})

    def get_deadtime(self):
        """ Gets the time to end term """
        pass

    def register_normalized(self):
        self.register_orig = self.register
        if self.register:
            self.register = self.register.replace('/', '')

    def slugfy(self):
        self.slug = '-'.join([self.title.lower(), self.register]) # TODO: fix it

    def __unicode__(self):
        return self.title[:20]

    def save(self, *args, **kwargs):
        self.register_normalized()
        self.slugfy()
        self.updated_at = datetime.datetime.now()
        super(Issue, self).save(*args, **kwargs)

    meta = {
            'allow_inheritance': True,
            'indexes': [ '-created_at', 'slug', {'fields': ['$body',
                        '$register_orig', '$title'],
                        'default_language': 'portuguese',
                        'weight': {'title':5, 'body':10, 'register_orig':3}}
                    ],
            'ordering': ['-created_at']
    }


class ScoreStars(db.EmbeddedDocument):
    #votes = db.IntField(default=0) len from listField equal votes
    score = db.IntField(default=0)
    voter = db.ReferenceField(User)


class Comment(db.Document):
    CHOICES_SOURCE = (
        (0, 'sc'),
        (1, 'sccd'),
        (2, 'email')
    )
    # if empty the comment is not associated with issue (or hashtag)
    issue_id = db.ReferenceField('Issue') # CASCADE ? Refactoring from issue_id to issue
    issue = db.ReferenceField('Issue') # CASCADE ? Refactoring from issue_id to issue
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField()
    shottime = db.StringField(default=None)
    body = db.StringField(verbose_name='Comment', required=True)
    author = db.ReferenceField('User', required=True)
    stars = db.ListField(db.EmbeddedDocumentField(ScoreStars))
    origin = db.IntField(choices=CHOICES_SOURCE, default=0)
    hashtags = db.ListField(db.StringField(max_length=120))
    title = db.StringField(max_length=255)
    mentions_users = db.ListField(db.StringField(max_length=120)) # It's User.shortname

    def set_shottime(self):
        """ Shottime is the time from event of the comment in minutes """
        if self.issue_id and self.shottime == None:
            deltatime = self.created_at - self.issue_id.created_at
            self.shottime = str(int(deltatime.total_seconds() / 60))

        if self.issue_id is None:
            self.shottime = str(datetime.datetime.today().hour) + 'h'

    def set_title(self):
        # Validation: It's required the users to provide comments with issue or
        # at least one hashtag within body message.
        if self.issue_id is None and len(self.hashtags) == 0:
            raise TypeError(u"It's required to provider an issue or hashtags")

        self.title = self.issue_id.title if self.issue_id else self.hashtags[0]

    def to_link_hashtag(self, hashtag):
        return '<a class="hashLink" eventname="hashtag-to-search" ' \
                    'colorlink="#47CACC" href="/hashtag/{value}">{value}' \
                    '</a>'.format(value=hashtag)

    def to_link_mention(self, shortname):
        return '<a class="mentions shortname username" href="/users/{value}">{value}</a>'.format(value=shortname)

    def set_hashtags(self):
        # TODO: to refactor to support update/edit a comment

        if len(self.hashtags) == 0:
            self.hashtags = re.findall(r'(#\w+)', self.body)
            # replacing text by link
            def macthaction(matchobj):
                if matchobj.group(0):
                    return self.to_link_hashtag(matchobj.group(0))

            self.body = re.sub(r'(#\w+)', macthaction, self.body)
        else:
            pass # clean links, format, etc. before...

    def set_users_mentioned(self):
        # TODO: to refactor to support update/edit a comment

        if len(self.mentions_users) == 0:
            self.mentions_users = re.findall(r'(@\w+)', self.body)
            # replacing text by link
            def macthaction(matchobj):
                if matchobj.group(0):
                    return self.to_link_mention(matchobj.group(0))

            self.body = re.sub(r'(@\w+)', macthaction, self.body)
        else:
            pass # clean links, format, etc. before...

    def has_mentions(self, shortname):
        pass
        # TODO: check if mentions_users contains shortname. Return boolean

    def to_json(self, current_user=None):
        data = self.to_mongo()

        if self.issue_id: # Eve to solve this approach.
            data['issue_id'] = {'Issue': {
                                    'title': self.issue_id.title,
                                    'register': self.issue_id.register
                                    }
                            }
        if getattr(self.author, 'shortname', False):
            username = self.author.shortname
        elif getattr(self.author, 'username', False):
            username = self.author.username
        else:
            username = "empty"

        if getattr(self.author, 'location', False):
            location = self.author.location
        else:
            location = None

        if getattr(self.author, 'avatar', False):
            avatar = self.author.avatar
        else:
            avatar = None

        if getattr(self.author, 'status_online', False):
            status_online = self.author.status_online
        else:
            status_online = None

        if getattr(self.author, 'md5_email', False):
            md5_email = self.author.md5_email
        else:
            md5_email = None

        data['author'] = {'User': {
                                'shortname': username,
                                'username': username,
                                'location': location,
                                'avatar': avatar,
                                'status_online': status_online,
                                'md5_email': md5_email
                        }
        }
        # Eve to solve this approach with DATE_FORMAT settings.
        day, month, year = self.created_at.day, self.created_at.month, self.created_at.year
        hour, minute = self.created_at.hour, self.created_at.minute
        data['created_at_human'] = "%sh%s %s/%s/%s" % (hour, minute, day, month, year)

        readOnly = False
        if self.stars and current_user:
            readOnly = current_user.email in [star_obj.voter.email for star_obj in self.stars]

        data['stars'] = {'votes': len(self.stars),
                    'score': sum([s.score for s in self.stars]),
                    'readOnly': readOnly
        }

        return json_util.dumps(data)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if 'created' in kwargs and kwargs['created']:
            publish_in_redis('comments', document.to_json()) # TODO: private comments

            # If has issue to publish in channel it.
            if document.issue_id:
                oid = str(document.issue_id.pk)
                channel = ''.join(['comments', oid])
                publish_in_redis(channel, document.to_json())


    meta = {
            'indexes': [ '-created_at', {'fields': ['$body',
                        '$author'],
                        'default_language': 'portuguese',
                        'weight': {'author':5, 'body':10}}
                    ],
            'ordering': ['-created_at'],
            'queryset_class': CustomQuerySet
    }

    def save(self, *args, **kwargs):
        self.set_shottime()
        self.set_hashtags()
        self.set_users_mentioned()
        self.set_title()
        super(Comment, self).save(*args, **kwargs)


class Tags(db.Document):
    tag = db.StringField(max_length=200);
    obj_linked = db.StringField(max_length=20, required=False) # It's objects linked with tag.
    obj_oid = db.StringField(required=False)
    obj_pk = db.StringField(required=False)


class Invite(db.Document):
    name = db.StringField(required=True, max_length=255)
    email = db.StringField(required=True, unique=False)
    invited_by_email = db.StringField(required=False, unique=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField()
    is_approved = db.BooleanField(default=False)
    used = db.BooleanField(default=False)
    # ObjectID alreay a token
    # TODO: #signals send to email

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if 'created' in kwargs and kwargs['created']:
            emails.request_invited(document.name, document.email)
        else:
            if document.is_approved and document.used == False:
                emails.approved_invited(document.name, document.email, document.pk)

# Signals pre_save
# ...
# Signals post_save
signals.post_save.connect(Issue.post_save, sender=Issue)
signals.post_save.connect(Comment.post_save, sender=Comment)
signals.post_save.connect(Invite.post_save, sender=Invite)
