from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import config.db
from schemas.citas import Cita, CitaCreate, CitaUpdate
from crud import usuarios as usuarioGet
from crud import citas as CitaCrud
from routes.usuarios import verify_token_simple  # Asegúrate de importar correctamente

cita_router = APIRouter()

def get_db():
    db = config.db.SesionLocal()
    try:
        yield db
    finally:
        db.close()

@cita_router.get("/citas/", response_model=List[Cita], tags=["Citas"])
def get_all_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_email: str = Depends(verify_token_simple)):
    return CitaCrud.get_all_citas(db, skip=skip, limit=limit)

@cita_router.get("/citas/usuario", response_model=List[Cita], tags=["Citas"])
def get_citas_usuario(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    user = usuarioGet.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return CitaCrud.get_citas_by_usuario(db, user_id=user.id, skip=skip, limit=limit)



from fastapi import Query  # Asegúrate de importar Query

@cita_router.post("/citas/", response_model=Cita, tags=["Citas"])
def create_cita(
    cita: CitaCreate, 
    user_id: int = Query(...),  # Ahora user_id es un parámetro de consulta (query)
    db: Session = Depends(get_db)
):
    # Obtenemos el usuario con el ID recibido en user_id
    user = usuarioGet.get_user_by_id(db, user_id=user_id)  # Esto buscará el usuario por su ID
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Ahora creamos la cita, pasando el ID del usuario correctamente
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
