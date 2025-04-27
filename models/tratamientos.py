from sqlalchemy import Column, Integer, String, Enum, Time
from sqlalchemy.orm import relationship
from config.db import Base
import enum

class EstatusTratamiento(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class Tratamiento(Base):
    __tablename__ = "tbb_tratamientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    estatus = Column(Enum(EstatusTratamiento), default=EstatusTratamiento.Activo, nullable=False)
    tiempo = Column(String(100), nullable=False) 
    
    cita = relationship("Cita", back_populates="tratamiento")

