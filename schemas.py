from pydantic import BaseModel
from typing import List

class MisionBase(BaseModel):
    descripcion: str
    xp: int

class MisionCreate(MisionBase):
    pass

class MisionOut(MisionBase):
    id: int

    class Config:
        from_attributes = True  

class PersonajeBase(BaseModel):
    nombre: str

class PersonajeCreate(PersonajeBase):
    pass

class PersonajeOut(PersonajeBase):
    id: int
    xp: int
    misiones: List[MisionOut] = []

    class Config:
        from_attributes = True 
