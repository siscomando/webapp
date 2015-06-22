# -*- coding: utf-8 -*-
import random
import sys

# Add local app
sys.path.append("../../app/")
from src import models

seed = random.randint(1000, 8000)
sups = ['SUPOP', 'SUPCD', 'SUPDE', 'SUNFJ', 'SUNNE', 'SUNAF', 'COTEC']
sort = random.randint(0, len(sups) - 1)
sistemas = ['SIGEPE (SUNMP)', 'CENTRO DE DADOS (SUPCD)', 'SIAPNET (SUNMP)', 
		'GUIA DE SERVIÇOS PÚBLICOS FEDERAL (SUNMP)', 'SICONV (SUNMP)', 
		'SIORG (SUNMP)', 'SOTN (SUNAF)', 'DESTNET (SUNMP)', 
		'TRANSPARENCIA PUBLICA CLIENTE (SUNFJ)', 'SNCR CCIR WEB (SUNCE)']
sort_sistemas = random.randint(0, len(sistemas) -1)
i = models.Issue()
i.body = 'Problema na conexão de... '
i.title = sistemas[sort_sistemas]
i.register = '2015RI/0000%s' % (str(seed))
i.ugat = sups[sort]
sort = random.randint(0, len(sups) - 1)
i.ugser = sups[sort]
i.save()

