from fastapi import APIRouter
from pydantic import BaseModel
from uuid import UUID, uuid4

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


@router.post("/")
def create_sudionik(sudionik: Sudionik):
    uuid = uuid4()
    return {
        "UUID": uuid,
        "Sudionik": f'{sudionik.ime} {sudionik.prezime}',
        "e-mail": sudionik.email,
        'telefon': sudionik.tel
    }
