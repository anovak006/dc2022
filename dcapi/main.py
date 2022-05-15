#! /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from .debugger import initialize_server_debugger_if_needed
from .routers import sudionik

initialize_server_debugger_if_needed()

app = FastAPI()

app.include_router(
    sudionik.router,
    prefix="/sudionik",
    tags=["sudionik"],
)


@app.get("/ping")
def pong():
    return {"ping": "PONG!"}
