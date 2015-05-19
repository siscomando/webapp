import datetime
import json
import md5
from flask import url_for
from mongoengine import signals, CASCADE, DENY
from flask.ext.mongoengine import BaseQuerySet
from bson import json_util
# APP
from src import database as db
from src import red
from src import login_manager

# SSE Events support
def publish_in_redis(channel, data):
    return red.publish(channel, data)

class CustomQuerySet(BaseQuerySet):
    def to_json(self):
        return "[%s]" % (','.join([doc.to_json() for doc in self]))

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    location = db.StringField(max_length=25)
    shortname = db.StringField(max_length=80)
    avatar = db.StringField()
    status_online = db.BooleanField(default=True)
    md5_email = db.StringField()

    meta = {'queryset_class': CustomQuerySet}    

    def to_json(self):
        data = self.to_mongo()
        data['password'] = None
        return json_util.dumps(data)    

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
        email = self.email.split('@')
        if len(email) == 2:
            self.set_shortname()
        else:
            raise TypeError('Mail address malformed')

    def set_shortname(self):
        self.shortname = self.email.split('@')[0]

    def save(self, *args, **kwargs):
        self.validate_email()
        self.set_shortname()
        self.md5_email = md5.md5(self.email).hexdigest()
        super(User, self).save(*args, **kwargs)


class Issue(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=False) # TODO slugfy
    body = db.StringField(required=True)
    register = db.StringField(max_length=120, required=True, unique=True)
    register_orig = db.StringField(max_length=120)
    classifier = db.IntField(default=0)
    ugat = db.StringField(max_length=12, required=True)
    ugser = db.StringField(max_length=12, required=True)
    deadline = db.IntField(default=120)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if 'created' in kwargs and kwargs['created']:
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


class Comment(db.Document):
    CHOICES_SOURCE = (
        (0, 'sc'), 
        (1, 'sccd'),
        (2, 'email')
    )
    # if empty the comment is not associated with issue (or hashtag)
    issue_id = db.ReferenceField('Issue', reverse_delete_rule=DENY)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    shottime = db.IntField(default=-1)
    body = db.StringField(verbose_name='Comment', required=True)
    author = db.ReferenceField('User', required=True, reverse_delete_rule=DENY)
    stars = db.IntField(default=0)
    origin = db.IntField(choices=CHOICES_SOURCE, default=0)
    # We can denormalization. See more 1-2-3 by starting here:
    # http://blog.mongodb.org/post/87200945828/6-rules-of-thumb-for-mongodb-schema-design-part-1

    def set_shottime(self):
        """ Shottime is the time from event of the comment in minutes """
        if self.issue_id and self.shottime == -1:
            deltatime = self.created_at - self.issue_id.created_at
            self.shottime = deltatime.total_seconds() / 60 

    def to_json(self):
        data = self.to_mongo()

        if self.issue_id:
            data['issue_id'] = {'Issue': {
                                    'title': self.issue_id.title, 
                                    'register': self.issue_id.register
                                    }
                            }
        data['author'] = {'User': {
                                'shortname': self.author.shortname,
                                'location': self.author.location,
                                'avatar': self.author.avatar,
                                'status_online': self.author.status_online,
                                'md5_email': self.author.md5_email
                        }
        }
        day, month, year = self.created_at.day, self.created_at.month, self.created_at.year  
        hour, minute = self.created_at.hour, self.created_at.minute
        data['created_at_human'] = "%sh%s %s/%s/%s" % (hour, minute, day, month, year)
              
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
        super(Comment, self).save(*args, **kwargs)


class Tags(db.Document):
    tag = db.StringField(max_length=200);
    obj_linked = db.StringField(max_length=20, required=False) # It's objects linked with tag.
    obj_oid = db.StringField(required=False)
    obj_pk = db.StringField(required=False)


# Signals
signals.post_save.connect(Issue.post_save, sender=Issue)
signals.post_save.connect(Comment.post_save, sender=Comment)

