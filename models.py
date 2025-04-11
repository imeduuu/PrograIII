from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    xp = Column(Integer, default=0)

    misiones = relationship("Mision", back_populates="personaje", cascade="all, delete-orphan")

class Mision(Base):
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    
    xp = Column(Integer)

    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    personaje = relationship("Personaje", back_populates="misiones")
