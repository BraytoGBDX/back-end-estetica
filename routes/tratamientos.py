from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import config.db
from schemas.tratamientos import Tratamiento, TratamientoCreate, TratamientoUpdate
from crud import tratamientos as TratamientoCrud
from routes.usuarios import verify_token_simple  # Asegúrate de que esta función esté bien importada

tratamiento_router = APIRouter()

def get_db():
    db = config.db.SesionLocal()
    try:
        yield db
    finally:
        db.close()

@tratamiento_router.get("/tratamientos/", response_model=List[Tratamiento], tags=["Tratamientos"])
def get_all_tratamientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    return TratamientoCrud.get_all_tratamientos(db, skip=skip, limit=limit)

@tratamiento_router.get("/tratamientos/{tratamiento_id}", response_model=Tratamiento, tags=["Tratamientos"])
def get_tratamiento_by_id(tratamiento_id: int, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    tratamiento = TratamientoCrud.get_tratamiento_by_id(db, tratamiento_id)
    if tratamiento is None:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tratamiento

@tratamiento_router.post("/tratamientos/", response_model=Tratamiento, tags=["Tratamientos"])
def create_tratamiento(tratamiento: TratamientoCreate, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    return TratamientoCrud.create_tratamiento(db, tratamiento)

@tratamiento_router.put("/tratamientos/{tratamiento_id}", response_model=Tratamiento, tags=["Tratamientos"])
def update_tratamiento(tratamiento_id: int, tratamiento: TratamientoUpdate, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    db_tratamiento = TratamientoCrud.get_tratamiento_by_id(db, tratamiento_id)
    if db_tratamiento is None:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return TratamientoCrud.update_tratamiento(db, tratamiento_id, tratamiento)

@tratamiento_router.delete("/tratamientos/{tratamiento_id}", tags=["Tratamientos"])
def delete_tratamiento(tratamiento_id: int, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    deleted = TratamientoCrud.delete_tratamiento(db, tratamiento_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return {"message": "Tratamiento eliminado correctamente"}
