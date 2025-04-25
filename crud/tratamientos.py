from sqlalchemy.orm import Session
from models.tratamientos import Tratamiento as TratamientoModel
from schemas.tratamientos import TratamientoCreate, TratamientoUpdate

# Obtener un tratamiento por ID
def get_tratamiento_by_id(db: Session, tratamiento_id: int):
    return db.query(TratamientoModel).filter(TratamientoModel.id == tratamiento_id).first()

# Obtener todos los tratamientos
def get_all_tratamientos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TratamientoModel).offset(skip).limit(limit).all()

# Crear un nuevo tratamiento
def create_tratamiento(db: Session, tratamiento: TratamientoCreate):
    db_tratamiento = TratamientoModel(
        nombre=tratamiento.nombre,
        descripcion=tratamiento.descripcion,
        estatus=tratamiento.estatus,
        tiempo=tratamiento.tiempo
    )
    db.add(db_tratamiento)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

# Actualizar un tratamiento
def update_tratamiento(db: Session, tratamiento_id: int, tratamiento: TratamientoUpdate):
    db_tratamiento = get_tratamiento_by_id(db, tratamiento_id)
    if db_tratamiento is None:
        return None
    for key, value in tratamiento.dict(exclude_unset=True).items():
        setattr(db_tratamiento, key, value)
    db.commit()
    db.refresh(db_tratamiento)
    return db_tratamiento

# Eliminar un tratamiento
def delete_tratamiento(db: Session, tratamiento_id: int):
    db_tratamiento = get_tratamiento_by_id(db, tratamiento_id)
    if db_tratamiento is None:
        return False
    db.delete(db_tratamiento)
    db.commit()
    return True
