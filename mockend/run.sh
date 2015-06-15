#!/bin/bash
gunicorn -w 4 -b 127.0.0.1:9003 --worker-class='gunicorn.workers.ggevent.GeventWorker' src:app
