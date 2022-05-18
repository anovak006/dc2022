#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import time
from celery import current_task
from celery.utils.log import get_task_logger
from celery.signals import task_prerun, task_postrun

from .main import celery_app


TASK_WITH_LOGGING = [
    'dcworker.worker.hard_work'
]


@task_prerun.connect
def task_prerun(task_id=None, task=None, args=None, **kwargs):
    if task.name in TASK_WITH_LOGGING:
        logger = get_task_logger(task_id)
        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s] %(message)s'
        )
        task_handler = logging.FileHandler(
            os.path.join('/var/log/dcworker', task_id+'.log')
        )
        task_handler.setFormatter(formatter)
        task_handler.setLevel(logging.INFO)
        logger.addHandler(task_handler)


@task_postrun.connect
def task_postrun(task_id=None, task=None, args=None, **kwargs):
    # getting the same logger and closing all handles associated with it
    logger = get_task_logger(task_id)
    for handler in logger.handlers:
        handler.flush()
        handler.close()
    logger.handlers = []


@celery_app.task(acks_late=True)
def hard_work(command: str, mult: int):
    logger = get_task_logger(current_task.request.id)

    logger.info(
        f'Treba obaviti jako težak zadatak {command}'
        f'koji traži {mult} ponavljanja!'
    )

    for i in range(mult):
        percent = 100*i/mult
        meta = {
            'realizirano': f'{percent:.2f}%',
            'zadatak': i,
            'ukupno_zadataka': mult
        }
        logger.info(f"state: PROGRESS, meta: {meta}")
        current_task.update_state(state='PROGRESS', meta=meta)
        time.sleep(1.0)
    logger.info(
        f'Izvršen zadatak: {command}. Napravljeno je {mult} ponavljanja.'
    )
    return {
        'message': (
            f'Izvršen zadatak: {command}.'
            f'Napravljeno je {mult} ponavljanja.'
        )
    }
