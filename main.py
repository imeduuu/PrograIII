from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from cola import ColaDeMisiones

app = FastAPI()

Base.metadata.create_all(bind=engine)

colas = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/personajes", response_model=schemas.PersonajeOut)
def crear_personaje(personaje: schemas.PersonajeCreate, db: Session = Depends(get_db)):
    nuevo = models.Personaje(nombre=personaje.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    colas[nuevo.id] = ColaDeMisiones()  
    return nuevo

@app.post("/misiones", response_model=schemas.MisionOut)
def crear_mision(mision: schemas.MisionCreate, db: Session = Depends(get_db)):
    nueva = models.Mision(**mision.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    personaje = db.query(models.Personaje).get(personaje_id)
    mision = db.query(models.Mision).get(mision_id)
    if not personaje or not mision:
        raise HTTPException(status_code=404, detail="Personaje o misión no encontrada")

    orden_actual = db.query(models.PersonajeMision)\
        .filter_by(personaje_id=personaje_id)\
        .count()

    relacion = models.PersonajeMision(
        personaje_id=personaje_id,
        mision_id=mision_id,
        orden=orden_actual
    )
    db.add(relacion)
    db.commit()

    return {"mensaje": f"Misión '{mision.descripcion}' aceptada por {personaje.nombre}"}


@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.query(models.Personaje).get(personaje_id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    relacion = db.query(models.PersonajeMision)\
        .filter_by(personaje_id=personaje_id)\
        .order_by(models.PersonajeMision.orden.asc())\
        .first()

    if not relacion:
        raise HTTPException(status_code=400, detail="No hay misiones por completar")

    mision = relacion.mision
    personaje.xp += mision.xp

    db.delete(relacion)
    db.commit()

    return {"mensaje": f"{personaje.nombre} completó '{mision.descripcion}' y ganó {mision.xp} XP"}


@app.get("/personajes/{personaje_id}/misiones", response_model=list[schemas.MisionOut])
def listar_misiones(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.query(models.Personaje).get(personaje_id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")

    relaciones = db.query(models.PersonajeMision)\
        .filter_by(personaje_id=personaje_id)\
        .order_by(models.PersonajeMision.orden.asc())\
        .all()

    return [relacion.mision for relacion in relaciones]

