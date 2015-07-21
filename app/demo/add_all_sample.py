# -*- coding: utf-8 -*-
import random
import sys
sys.path.append('../../app')
from siscomando import models

QTD_USERS = 50
sups = ['SUPOP', 'SUPCD', 'SUPDE', 'SUNFJ', 'SUNNE', 'SUNAF', 'COTEC']
sistemas = ['SIGEPE (SUNMP)', 'CENTRO DE DADOS (SUPCD)', 'SIAPNET (SUNMP)', 
		'GUIA DE SERVIÇOS PÚBLICOS FEDERAL (SUNMP)', 'SICONV (SUNMP)', 
		'SIORG (SUNMP)', 'SOTN (SUNAF)', 'DESTNET (SUNMP)', 
		'TRANSPARENCIA PUBLICA CLIENTE (SUNFJ)', 'SNCR CCIR WEB (SUNCE)']
people = ['Joao', 'Antonio', 'Maria', 'DoCarmo', 'Caetano', 'Vinicius', 'Tom',
        'Juarez', 'Abidoral', 'Clerio', 'Sandra Rosa', 'Madelena', 'Jacilda']

# Adding users...
for i in range(1, QTD_USERS):
    name = people[random.randint(0, len(people) - 1)]
    lastname = people[random.randint(0, len(people) - 1)]
    email = ''.join([name, lastname, '_', str(i), '@', lastname, '.com'])
    u = models.User()
    u.email = email
    u.password = '123'
    u.save()

# Adding systems...
bodies = [
        'Interactively deploy backward-compatible processes rather than premier #mindshare. ',
    'Dramatically transform client-focused data for leveraged internal',
    'Dramatically transform client-focused data for #leveraged internal or "organic" sources. Globally optimize just in time portals without backward-compatible functionalities. Quickly seize enabled customer service rather than resource sucking web-readiness. ',
    'Enthusiastically drive premier partnerships after premier web-readiness. Collaboratively reinvent maintainable products after cross functional schemas. Authoritatively enhance flexible e-services and team driven results.',
    'Monotonectally customize team driven mindshare rather than leading-edge collaboration and idea-sharing. Energistically fashion front-end partnerships vis-a-vis leading-edge niches. Rapidiously transform holistic synergy via unique value. ',
    'Continually procrastinate progressive results whereas cooperative imperatives.',
    'Progressively formulate client-centered interfaces without just in time e-business. #Progressively utilize maintainable value rather than turnkey human capital. Enthusiastically envisioneer synergistic supply chains for inexpensive innovation.',
    'Professionally e-enable bricks-and-clicks opportunities before granular total linkage. Synergistically predominate frictionless methodologies before ',
    'Conveniently underwhelm alternative web services vis-a-vis team building services'
]

users = models.User.objects()

for s in range(1, 50):
    sort = random.randint(0, len(sups) - 1)
    seed = random.randint(1000, 8000)
    i = models.Issue()
    i.body = 'Problema na conexão de... '
    sort_sistemas = random.randint(0, len(sistemas) -1)
    i.title = sistemas[sort_sistemas]
    i.register = '2015RI/{}{}'.format(str(seed), s)
    i.ugat = sups[sort]
    sort = random.randint(0, len(sups) - 1)
    i.ugser = sups[sort]
    i.author = users[0]
    i.save(i)
    
    for f in range(1, 20):
        ord_users = random.randint(0, len(users) - 1)
        st = models.ScoreStars(score=random.randint(1,5), 
            voter=users[ord_users])
        print st.score, st.voter
        comment = models.Comment()
        comment.issue_id = i
        comment.body = bodies[random.randint(0, len(bodies) -1)]
        comment.author = users[random.randint(0, QTD_USERS - 2)]
        comment.stars.append(st)
        comment.save()



