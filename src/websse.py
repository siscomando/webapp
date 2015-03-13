# -*- coding: utf-8 -*- 
"""
This is a generator of tickets to SisComando.
created by horacioibrahim at gmail dot com
"""

import time, datetime, random, json
from gevent import monkey; monkey.patch_all()
from gevent import sleep
from bottle import get, post, request, response
from bottle import GeventServer, run

# The decorator for CORS
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept,' \
                                'Content-Type, X-Requested-With, X-CSRF-Token' 
                                
        if request.method != 'OPTIONS':
            # actula request; reply with actual response
            return fn(*args, **kwargs)       

    return _enable_cors

def generator_issues():
    date_at = datetime.date.strftime(datetime.datetime.now(), '%d/%m/%Y %Hh%M')
    register = "2015RI/00000%i" % random.randint(1, 10000)
    tittle_choose = random.randint(0, 4)
    title_sample = ["SICAP - SISTEMA", "ALM - GERENCIAMENTO", "EXPRESSO SERPRO",
    "SIXEN - SISTEMA XEN", "SISEP - SEP MANAG"]
    icon = random.randint(0, 2)

    issue = {"register": register, "title": title_sample[tittle_choose], 
    "uga": "SUPGS", "ugs": "SUNCE", "date": date_at, "icon": icon}    

    return json.dumps(issue)

@get('/stream')
@enable_cors
def stream():
    response.content_type = 'text/event-stream'
    response.cache_control = 'no-cache'

    # Set client side auto reconnect timeout, ms.
    yield 'retry: 100\n\n'

    # keep connection alive n more then ... (s)
    end = time.time() + 60
    issue = generator_issues()
    while time.time() < end:
        yield 'data: %s\n\n' % issue
        yield 'event: userlogon\n'
        yield 'data: %s\n\n' % "horacioibrahim"
        sleep(10)
        issue = generator_issues()

if __name__ == '__main__':
    run(server=GeventServer)

