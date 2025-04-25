from pydantic import BaseModel
from datetime import datetime, time, date
from typing import Optional

class CitaBase(BaseModel):
    idUsuario: int  # ID del usuario que hace la cita
    idTratamiento: int
    estatus: str
    horario: time
    fecha: date

    class Config:
        from_attributes = True

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    tratamiento: Optional[str] = None
    estatus: Optional[str] = None
    horario: Optional[time] = None
    fecha: Optional[date] = None

    class Config:
        from_attributes = True

class Cita(CitaBase):
    id: int

    class Config:
        from_attributes = True
