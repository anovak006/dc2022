#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from .connector import Base


class Sudionik(Base):
    __tablename__ = 'sudionik'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, unique=True)
    ime = Column(String)
    prezime = Column(String)
    email = Column(String, unique=True)
    tel = Column(String)
    aktivnosti = relationship('AktivnostSudionika', back_populates='sudionik')


class Aktivnost(Base):
    __tablename__ = 'aktivnost'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, unique=True)
    naziv = Column(String)
    opis = Column(String)
    pocetak = Column(DateTime)
    kraj = Column(DateTime)
    sudionici = relationship('AktivnostSudionika', back_populates='aktivnost')


class AktivnostSudionika(Base):
    __tablename__ = 'aktivnost_sudionika'
    sudionik_id = Column(ForeignKey('sudionik.id'), primary_key=True)
    aktivnost_id = Column(ForeignKey('aktivnost.id'), primary_key=True)
    sudionik = relationship('Sudionik', back_populates='aktivnosti')
    aktivnost = relationship('Aktivnost', back_populates='sudionici')
