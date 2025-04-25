from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from schemas.citas import Cita, CitaCreate, CitaUpdate
from crud import citas as CitaCrud
from routes.usuarios import verify_token_simple  # Asegúrate de importar correctamente

cita_router = APIRouter()

@cita_router.get("/citas/", response_model=List[Cita], tags=["Citas"])
def get_all_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    return CitaCrud.get_all_citas(db, skip=skip, limit=limit)

@cita_router.get("/citas/usuario", response_model=List[Cita], tags=["Citas"])
def get_citas_usuario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    user = CitaCrud.get_user_by_email(db, email=user_email)
    return CitaCrud.get_citas_by_usuario(db, user_id=user.id, skip=skip, limit=limit)

@cita_router.post("/citas/", response_model=Cita, tags=["Citas"])
def create_cita(cita: CitaCreate, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    user = CitaCrud.get_user_by_email(db, email=user_email)
    return CitaCrud.create_cita(db, cita=cita, user_id=user.id)

@cita_router.put("/citas/{cita_id}", response_model=Cita, tags=["Citas"])
def update_cita(cita_id: int, cita: CitaUpdate, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    db_cita = CitaCrud.get_cita_by_id(db, cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return CitaCrud.update_cita(db, cita_id, cita)

@cita_router.delete("/citas/{cita_id}", tags=["Citas"])
def delete_cita(cita_id: int, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    deleted = CitaCrud.delete_cita(db, cita_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"message": "Cita eliminada correctamente"}
