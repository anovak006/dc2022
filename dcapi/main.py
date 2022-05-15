#! /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from .debugger import initialize_server_debugger_if_needed
initialize_server_debugger_if_needed()

app = FastAPI()



@app.get("/ping")
def pong():
    return {"ping": "PONG!"}
