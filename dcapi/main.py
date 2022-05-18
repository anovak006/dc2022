#! /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from .debugger import initialize_server_debugger_if_needed
from .routers import sudionik, worker
from .redis import get_redis_pool

initialize_server_debugger_if_needed()

app = FastAPI()

app.include_router(
    sudionik.router,
    prefix="/sudionik",
    tags=["sudionik"],
)

app.include_router(
    worker.router,
    prefix="/worker",
    tags=["asinkroni zadaci"],
)


@app.on_event('startup')
def starup_event():
    app.state.pool, app.state.redis = get_redis_pool()


@app.on_event('shutdown')
async def shutdown_event():
    await app.state.pool.disconnect()


@app.get("/ping")
def pong():
    return {"ping": "PONG!"}
