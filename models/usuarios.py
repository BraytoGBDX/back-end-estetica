from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from config.db import Base
import enum

class TipoUsuario(str, enum.Enum):
    Cliente = "Cliente"
    Administrador = "Administrador"

class Estatus(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Bloqueado = "Bloqueado"

class User(Base):
    __tablename__ = "tbb_usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(60))
    apellidos = Column(String(60))
    tipoUsuario = Column(Enum(TipoUsuario))
    correoElectronico = Column(String(100))
    contrasena = Column(String(60))
    numeroTelefono = Column(String(20))
    estatus = Column(Enum(Estatus))
    fechaRegistro = Column(DateTime)
    fechaActualizacion = Column(DateTime)

    # 👇 back_populates debe coincidir con el de Cita
    cita = relationship("Cita", back_populates="usuario")
