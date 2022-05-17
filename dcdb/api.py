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


def dohvati_sudionika(
    db: Session,
    uuid: UUID
):
    try:
        sudionik = db.query(Sudionik).filter_by(uuid=uuid).one()
    except Exception:
        raise
    return sudionik


def nadopuni_sudionika(
    db: Session,
    uuid: UUID,
    ime: str = None,
    prezime: str = None,
    email: str = None,
    tel: str = None
):
    try:
        sudionik = db.query(Sudionik).filter_by(uuid=uuid).one()
    except Exception:
        raise
    if ime:
        sudionik.ime = ime
    if prezime:
        sudionik.prezime = prezime
    if email:
        sudionik.email = email
    if tel:
        sudionik.tel = tel
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    return sudionik


def obrisi_sudionika(
    db: Session,
    uuid: UUID,
):
    try:
        sudionik = db.query(Sudionik).filter_by(uuid=uuid).one()
        db.delete(sudionik)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return True


def potrazi_sudionika(
    db: Session,
    prezime: str,
    page: int = 1,
    limit: int = 20
):
    offset = (page - 1) * limit
    try:
        result = (
            db.query(Sudionik.ime, Sudionik.prezime,
                     Sudionik.email, Sudionik.tel, Sudionik.uuid)
              .select_from(Sudionik)
              .filter(Sudionik.prezime.ilike(f'{prezime}%'))
              .order_by(func.similarity(Sudionik.prezime, prezime).desc())
              .limit(limit).offset(offset).all()
        )
        query = db.query(func.count(Sudionik.id))\
                  .filter(Sudionik.prezime.ilike(f'{prezime}%'))
        count = query.scalar()
    except NoResultFound:
        return False
    return count, result
