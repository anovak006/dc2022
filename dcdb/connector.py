# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
db_name = os.environ["POSTGRES_DB"]
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = (f"postgresql://{user}:{password}"
                           f"@dors2022_db_1/{db_name}")


def dumps(d):
    return json.dumps(d, default=str)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    json_serializer=dumps
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
