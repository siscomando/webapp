#!/bin/bash
gunicorn -w 4 -b 0.0.0.0:9003 --worker-class='gunicorn.workers.ggevent.GeventWorker' src:app
