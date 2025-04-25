from sqlalchemy.orm import Session
from datetime import datetime
from models.citas import Cita as CitaModel
from schemas.citas import CitaCreate, CitaUpdate

# Obtener una cita por ID
def get_cita_by_id(db: Session, cita_id: int):
    return db.query(CitaModel).filter(CitaModel.id == cita_id).first()

# Obtener todas las citas en general
def get_all_citas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CitaModel).offset(skip).limit(limit).all()

# Obtener todas las citas de un usuario
def get_citas_by_usuario(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(CitaModel).filter(CitaModel.idUsuario == user_id).offset(skip).limit(limit).all()

# Crear una nueva cita
def create_cita(db: Session, cita: CitaCreate, user_id: int):
    db_cita = CitaModel(
        idUsuario=user_id,
        tratamiento=cita.tratamiento,
        estatus=cita.estatus,
        horario=cita.horario,
        fecha=cita.fecha
    )
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

# Actualizar una cita
def update_cita(db: Session, cita_id: int, cita: CitaUpdate):
    db_cita = get_cita_by_id(db, cita_id)
    if db_cita is None:
        return None
    for key, value in cita.dict(exclude_unset=True).items():
        setattr(db_cita, key, value)
    db.commit()
    db.refresh(db_cita)
    return db_cita

# Eliminar una cita
def delete_cita(db: Session, cita_id: int):
    db_cita = get_cita_by_id(db, cita_id)
    if db_cita is None:
        return False
    db.delete(db_cita)
    db.commit()
    return True
