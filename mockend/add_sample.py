# -*- coding: utf-8 -*-
import random
from src import models

seed = random.randint(1000, 8000)
sups = ['SUPOP', 'SUPCD', 'SUPDE', 'SUNFJ', 'SUNNE', 'SUNAF', 'COTEC']
sort = random.randint(0, len(sups) - 1)
sistemas = ['ALM - SISTEMA', 'SICAF', 'SIAFI', 'EXPRESSO', 'SISCOR', 'SICOV', 'SISCOMEX']
sort_sistemas = random.randint(0, len(sistemas) -1)
i = models.Issue()
i.body = 'Problema na conexão de... '
i.title = sistemas[sort_sistemas]
i.register = '2015RI/0000%s' % (str(seed))
i.ugat = sups[sort]
sort = random.randint(0, len(sups) - 1)
i.ugser = sups[sort]
i.save()

