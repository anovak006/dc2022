#! /usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
import os
from .debugger import initialize_server_debugger_if_needed

initialize_server_debugger_if_needed()

celery_app = Celery(
    "dc2022",
    backend=f"redis://:{os.environ.get('REDIS_PASS')}@dc2022_redis:6379/0",
    broker=f"amqp://{os.environ.get('RABBITMQ_USER')}:"
           f"{os.environ.get('RABBITMQ_PASS')}@dc2022_rabbitmq:5672/"
           f"{os.environ.get('RABBITMQ_DEFAULT_VHOST')}",
    redbeat_redis_url="redis://:{os.environ.get('REDIS_PASS')}@dc2022_redis:6379/1",
    include=['dcworker.worker']
)

celery_app.conf.task_routes = {
    "dcworker.worker.hard_work": "dc2022"
}
celery_app.conf.update(task_track_started=True)
