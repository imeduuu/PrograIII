from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    xp = Column(Integer, default=0)

    misiones = relationship("PersonajeMision", back_populates="personaje", cascade="all, delete-orphan")

class Mision(Base):
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    xp = Column(Integer)

    personajes = relationship("PersonajeMision", back_populates="mision", cascade="all, delete-orphan")

class PersonajeMision(Base):
    __tablename__ = "personaje_mision"

    id = Column(Integer, primary_key=True, index=True)
    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    mision_id = Column(Integer, ForeignKey("misiones.id"))
    orden = Column(Integer) 

    personaje = relationship("Personaje", back_populates="misiones")
    mision = relationship("Mision", back_populates="personajes")
