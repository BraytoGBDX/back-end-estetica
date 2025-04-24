from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONFIG")

# Crear el motor (engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Crear la sesión
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir el objeto base para los modelos
Base = declarative_base()

