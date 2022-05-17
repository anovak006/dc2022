# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from uuid import uuid4, UUID

from .models import (
    Sudionik
)


def kreiraj_sudionika(
    db: Session,
    ime: str,
    prezime: str,
    email: str = None,
    tel: str = None
):
    '''
    Create participant

    Params
    ------

    db: Session
    ime: 'Ime',
    prezime: 'Prezime',
    email: 'korisnicko.ime@domena.hr': None,
    tel: 'tel 091 123 4567': None}
    '''
    uuid = uuid4()
    try:
        sudionik = Sudionik(
            uuid=uuid,
            ime=ime,
            prezime=prezime,
            email=email,
            tel=tel
        )
        db.add(sudionik)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return sudionik


