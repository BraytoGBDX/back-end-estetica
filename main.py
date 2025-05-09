from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import engine, Base, SesionLocal
from models.usuarios import User 
from models.citas import Cita
from models.tratamientos import Tratamiento
from crud.createAdmin import create_default_admin
from routes.usuarios import user
from routes.citas import cita_router
from routes.tratamientos import tratamiento_router

app = FastAPI(
    title="Example S.A de C.V",
    description="API de prueba para almacenar usuarios"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Al iniciar la app
@app.on_event("startup")
def startup_event():
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)

    # Crear usuario admin predefinido
    db = SesionLocal()
    create_default_admin(db)
    db.close()
    
app.include_router(user)
app.include_router(cita_router)
app.include_router(tratamiento_router)

