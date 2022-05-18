#! /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
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


@app.post("/redis", status_code=201)
async def create_redis_record(
    naziv: str,
    vrijednost: str,
    vrijeme: int = 30
):
    try:
        await app.state.redis.setex(naziv, vrijeme, vrijednost)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')


@app.get("/redis/{naziv}")
async def read_redis_record(naziv: str):
    try:
        vrijednost = await app.state.redis.get(naziv)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')
    return {"naziv_varijable": naziv, "vrijednost_varijable": vrijednost}


@app.delete("/redis/{naziv}", status_code=204)
async def delete_redis_record(naziv: str):
    try:
        if await app.state.redis.get(naziv):
            await app.state.redis.delete(naziv)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')
