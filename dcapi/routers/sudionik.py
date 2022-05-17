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
)

router = APIRouter()


class Sudionik(BaseModel):
    ime: str
    prezime: str
    email: str
    tel: str


@router.get("/{uuid}")
def read_sudionik(uuid: UUID):
    return {"UUID": uuid, "Podaci": 'Nema zapisa'}


@router.put("/{uuid}")
def update_sudionik(uuid: UUID, sudionik: Sudionik):
    return {
        "UUID": uuid,
        "Sudionik": f'{sudionik.ime} {sudionik.prezime}',
        "e-mail": sudionik.email,
        'telefon': sudionik.tel
    }


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
        raise HTTPException(status_code=500, detail=e)
