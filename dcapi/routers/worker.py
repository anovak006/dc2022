#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import (
    APIRouter, HTTPException, BackgroundTasks,
    Path, Query
)
from uvicorn.config import logger
from celery.result import GroupResult, AsyncResult

# Local imports
from dcworker.main import celery_app

router = APIRouter()


def on_raw_message(body):
    logger.info(body)


def task_result(result):
    logger.info(result.get(on_message=on_raw_message, propagate=False))


@router.get('/task-status/{result_id}')
async def get_task_status(
    result_id: str = Path(..., title='Celery Result ID'),
    group_of_tasks: bool = Query(False)
):
    if group_of_tasks:
        all_successful = False
        tasks_result = None
        result = GroupResult.restore(result_id, app=celery_app)

        if result:
            tasks_executed = result.completed_count()
            if result.ready():
                # Because error in Celery we use result.join instead result.get
                # https://github.com/celery/celery/issues/5359
                # https://github.com/celery/celery/issues/5359
                tasks_result = result.join(timeout=3)
                all_successful = result.successful()
            return {
                'group_of_tasks': result_id,
                'tasks_executed': tasks_executed,
                'all_successful': all_successful,
                'tasks_result': tasks_result
            }
        else:
            return {
                'group_of_tasks': 'Invalid',
                'tasks_executed': None,
                'all_successful': None,
                'tasks_result': None
            }
    else:
        result = AsyncResult(result_id, app=celery_app)
        if result:
            uuid = result.id
            status = result.status
            successful = result.successful()
            return {
                'uuid': uuid,
                'status': status,
                'successful': successful
            }
        else:
            # ToDo Dohvati rezultat iz baze
            return {
                'uuid': None,
                'status': None,
                'successful': None
            }


@router.post('/hard-work', status_code=202)
async def hard_work(
    background_task: BackgroundTasks,
    command: str,
    mult: int = 1
):

    task_parameters = {
        "command": command,
        "mult": mult
    }

    try:
        result = celery_app.send_task(
            "dcworker.worker.hard_work",
            kwargs=task_parameters
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')

    background_task.add_task(task_result, result)
    return {
        "message": {
            "command": command,
            "mult": mult,
            "uuid": result.id,
            "status": result.status,
            "successful": result.successful()
        }
    }
