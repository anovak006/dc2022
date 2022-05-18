from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID
from typing import List

from dcapi.helpers import get_db
from dcdb.api import (
    kreiraj_sudionika,
    dohvati_sudionika,
    nadopuni_sudionika,
    obrisi_sudionika,
    potrazi_sudionika,
)

router = APIRouter()


class Sudionik(BaseModel):
    ime: str
    prezime: str
    email: str
    tel: str


class SudionikNone(BaseModel):
    ime: str = None
    prezime: str = None
    email: str = None
    tel: str = None


class SudionikUUID(Sudionik):
    uuid: UUID

    class Config:
        orm_mode = True


class SudionikSearchResults(BaseModel):
    ukupno_rezultata: int
    sudionici: List[SudionikUUID]

    class Config:
        orm_mode = True


@router.get('/search', response_model=SudionikSearchResults)
async def search_sudionik(
    prezime: str = Query(..., min_length=1),
    page: int = Query(1, gt=0),
    limit: int = Query(1, gt=0),
    db: Session = Depends(get_db)
) -> SudionikSearchResults:
    try:
        ukupno, sudionici = potrazi_sudionika(
            db, prezime, page, limit
        )
    except Exception as e:
        raise e
    return {'ukupno_rezultata': ukupno, 'sudionici': sudionici}


@router.get("/{uuid}", response_model=SudionikUUID)
async def read_sudionik(
    uuid: UUID,
    db: Session = Depends(get_db)
):
    try:
        sudionik = dohvati_sudionika(db, uuid)
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail=f"Sudionik s UUID: {uuid} ne postoji!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')
    del sudionik.id
    return sudionik


@router.put("/{uuid}")
async def update_sudionik(
    uuid: UUID,
    sudionik: SudionikNone,
    db: Session = Depends(get_db)
):
    try:
        sudionik = nadopuni_sudionika(db, uuid, **sudionik.__dict__)
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail=f"Sudionik s UUID: {uuid} ne postoji!")
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Sudionik s email adresom: {sudionik.email} već postoji!"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')
    del sudionik.id
    return sudionik


@router.post("/", status_code=201)
async def create_sudionik(
    sudionik: Sudionik,
    db: Session = Depends(get_db)
):
    try:
        sudionik = kreiraj_sudionika(db, **sudionik.__dict__)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Sudionik s email adresom: {sudionik.email} već postoji!"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')
    return {"UUID": sudionik.uuid}


@router.delete("/{uuid}", status_code=204)
async def delete_sudionik(
    uuid: UUID,
    db: Session = Depends(get_db)
):
    try:
        obrisi_sudionika(db, uuid)
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail=f"Sudionik s UUID: {uuid} ne postoji!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{e.__doc__} {str(e)}')
