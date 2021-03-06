#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    vscode_debug_port: int = Field(10002, env="VSCODE_DEBUG_PORT")
    debugger: str = Field("", env="DEBUGGER")
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")
    redis_pass: str = Field("", env="REDIS_PASS")

    class Config:
        env_file = ".env"


settings = Settings()
