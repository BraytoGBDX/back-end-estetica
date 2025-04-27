from pydantic import BaseModel
from datetime import time
from typing import Optional
from enum import Enum

class Estatus(str, Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Bloqueado = "Bloqueado"

class TratamientoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estatus: Estatus
    tiempo: str

    class Config:
        from_attributes = True

class TratamientoCreate(TratamientoBase):
    pass

class TratamientoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estatus: Optional[Estatus] = None
    tiempo: Optional[str] = None

    class Config:
        from_attributes = True

class Tratamiento(TratamientoBase):
    id: int

    class Config:
        from_attributes = True
