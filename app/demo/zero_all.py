# -*- coding: utf-8 -*-
import random
from src import models

cs = models.Comment.objects()
for c in cs:
    c.delete()
issues = models.Issue.objects()
for i in issues:
    i.delete()

