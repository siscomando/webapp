# -*- coding: utf-8 -*-
from siscomando import models

cs = models.Comment.objects()
for c in cs:
    c.delete()
issues = models.Issue.objects()
for i in issues:
    i.delete()

