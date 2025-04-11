from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class PersonajeMision(Base):
    __tablename__ = 'personaje_mision'

    id = Column(Integer, primary_key=True, index=True)
    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    mision_id = Column(Integer, ForeignKey("misiones.id"))
    orden = Column(Integer)

    personaje = relationship("Personaje", back_populates="relaciones")
    mision = relationship("Mision")

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    xp = Column(Integer, default=0)
    
    misiones = relationship("Mision", secondary=PersonajeMision, back_populates="personajes")

class Mision(Base):
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    xp = Column(Integer)

    personajes = relationship("Personaje", secondary=PersonajeMision, back_populates="misiones")
