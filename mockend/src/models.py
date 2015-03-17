import datetime
from flask import url_for

# APP
from src import database as db

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
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('issue', kwargs={'slug': self.slug})

    def get_deadtime(self):
        """ Gets the time to end term """
        pass

    def register_normalized(self):
        self.register_orig = self.register
        self.register = self.register.replace('/', '')

    def __unicode__(self):
        return self.title[:20]

    def save(self, *args, **kwargs):
        self.register_normalized()
        super(Issue, self).save(*args, **kwargs)

    meta = {
            'allow_inheritance': True,
            'indexes': ['-created_at', 'slug'],
            'ordering': ['-created_at']
    }


class Comment(db.EmbeddedDocument):
    CHOICES_SOURCE = (
        (0, 'sc'), 
        (1, 'sccd'),
        (2, 'email')
    )
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name='Comment', required=True)
    author = db.StringField(verbose_name='Name', max_length=120, required=True)
    stars = db.IntField()
    origin = db.IntField(choices=CHOICES_SOURCE)



