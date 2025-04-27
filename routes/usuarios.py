from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import crud.usuarios as UserCrud
import config.db
from schemas.usuarios import User, UserCreate, UserUpdate, UserLogin, Token
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Header
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_GOOGLE")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

user = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bearer_scheme = HTTPBearer()

def get_db():
    db = config.db.SesionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
        return idinfo
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de Google inválido o expirado"
        )

def verify_token_simple(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado o inválido",
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")  # Extraemos el id
        tipo_usuario = payload.get("tipoUsuario")  # Extraemos el tipoUsuario
        if user_id is None or tipo_usuario is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return {"user_id": user_id, "tipo_usuario": tipo_usuario}  # Regresamos tanto el ID como el tipo de usuario
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@user.post("/users/google-login", response_model=Token, tags=["Usuarios"])
async def login_with_google(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]  # Authorization: Bearer <token_id_google>
    idinfo = verify_google_token(token)  # Verificar el token de Google
    
    # Aquí creas o actualizas al usuario con los datos obtenidos de Google
    user_db = UserCrud.create_or_update_user_with_google(db, user_info=idinfo)
    
    # Ahora que tenemos el usuario, incluimos el campo 'tipoUsuario' en el payload del token
    access_token = create_access_token(data={
        "sub": user_db.correoElectronico,  # Correo electrónico del usuario
        "id": user_db.id,  # ID del usuario
        "tipoUsuario": user_db.tipoUsuario  # Tipo de usuario que debería estar en el modelo 'User'
    })
    
    return {"access_token": access_token, "token_type": "bearer"}


@user.post("/users/login", response_model=Token, tags=["Usuarios"])
async def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    # Verificar si el usuario existe en la base de datos
    user_db = UserCrud.get_user_by_email(db, correo=user.correoElectronico)
    if not user_db or not verify_password(user.contrasena, user_db.contrasena):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    # Aquí se incluye el campo 'tipoUsuario' en el payload del token
    access_token = create_access_token(data={
        "sub": user_db.correoElectronico,  # Correo electrónico del usuario
        "id": user_db.id,  # ID del usuario
        "tipoUsuario": user_db.tipoUsuario  # Tipo de usuario (asegúrate de que el modelo 'User' tenga este campo)
    })
    
    return {"access_token": access_token, "token_type": "bearer"}




@user.get('/users/', response_model=List[User], tags=['Usuarios'])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id_from_token: int = Depends(verify_token_simple)):
    return UserCrud.get_users(db=db, skip=skip, limit=limit)

@user.get("/users/{user_id}", response_model=User, tags=["Usuarios"])
async def get_user(user_id: int, db: Session = Depends(get_db), user_data_from_token: dict = Depends(verify_token_simple)):
    # Si el usuario es un administrador, permite ver cualquier usuario
    if user_data_from_token["tipo_usuario"] == "Administrador":
        user = UserCrud.get_user_by_id(db=db, user_id=user_id)
    else:
        # Si el usuario no es administrador, solo puede ver su propio perfil
        if user_id != user_data_from_token["user_id"]:
            raise HTTPException(status_code=403, detail="No autorizado para ver este usuario")
        user = UserCrud.get_user_by_id(db=db, user_id=user_data_from_token["user_id"])

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user



@user.post("/usersCreate/", response_model=User, tags=["Usuarios"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):  
    return UserCrud.create_user(db=db, user=user)

@user.put("/usersUpdate/{user_id}", response_model=User, tags=["Usuarios"])
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), user_id_from_token: int = Depends(verify_token_simple)):
    updated_user = UserCrud.update_user(db=db, user_id=user_id, user=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no se pudo actualizar")
    return updated_user

@user.delete("/usersDelete/{user_id}", tags=["Usuarios"])
async def delete_user(user_id: int, db: Session = Depends(get_db), user_id_from_token: int = Depends(verify_token_simple)):
    deleted = UserCrud.delete_user(db=db, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no se pudo eliminar")
    return {"message": "Usuario eliminado correctamente"}
