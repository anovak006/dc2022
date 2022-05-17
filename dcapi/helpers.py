# -*- coding: utf-8 -*-
from dcdb.connector import SessionLocal


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
