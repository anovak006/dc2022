#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    vscode_debug_port: int = Field(10002, env="VSCODE_DEBUG_PORT")
    debugger: str = Field("", env="DEBUGGER")

    class Config:
        env_file = ".env"


settings = Settings()
