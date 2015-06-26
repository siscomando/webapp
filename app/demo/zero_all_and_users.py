# -*- coding: utf-8 -*-
import sys
sys.path.append('../../app')
from siscomando import models

cs = models.Comment.objects()
for c in cs:
    c.delete()
issues = models.Issue.objects()
for i in issues:
    i.delete()

users = models.User.objects()
for u in users:
    u.delete()
