from sqlalchemy import Column, Integer, String, Time, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
import enum

class EstatusCita(str, enum.Enum):
    Pendiente = "Pendiente"
    Confirmada = "Confirmada"
    Cancelada = "Cancelada"

class Cita(Base):
    __tablename__ = "tbb_citas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer, ForeignKey("tbb_usuarios.id"), nullable=False)
    idTratamiento = Column(Integer, ForeignKey("tbb_tratamentos.id"), nullable=False)
    tratamiento = Column(String(100), nullable=False)
    estatus = Column(Enum(EstatusCita), default=EstatusCita.Pendiente, nullable=False)
    horario = Column(Time, nullable=False)
    fecha = Column(Date, nullable=False)

    usuario = relationship("User", back_populates="cita")
    tratamiento = relationship("Tratamiento", back_populates="cita")
