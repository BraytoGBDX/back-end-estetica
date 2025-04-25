from models.usuarios import User as UserModel
from schemas.usuarios import UserCreate, UserUpdate
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_id(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, correo: str):
    return db.query(UserModel).filter(UserModel.correoElectronico == correo).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserModel).offset(skip).limit(limit).all()

# Crear un nuevo usuario
def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        nombre=user.nombre,
        apellidos=user.apellidos,
        tipoUsuario=user.tipoUsuario,
        correoElectronico=user.correoElectronico,
        contrasena=get_password_hash(user.contrasena),  # Usamos el hash de la contraseña aquí
        numeroTelefono=user.numeroTelefono,
        estatus=user.estatus,
        fechaRegistro=datetime.utcnow(),
        fechaActualizacion=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Actualizar usuario
def update_user(db: Session, user_id: str, user: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
        
        db_user.fechaActualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar usuario
def delete_user(db: Session, user_id: str):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True
