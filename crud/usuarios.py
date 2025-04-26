from models.usuarios import User as UserModel
from schemas.usuarios import UserCreate, UserUpdate
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# En crud/usuarios.py
def create_or_update_user_with_google(db: Session, user_info: dict):
    # Buscar si el usuario ya existe por el correo electrónico
    db_user = db.query(UserModel).filter(UserModel.correoElectronico == user_info['email']).first()

    if db_user:
        # Si el usuario ya existe, actualizar los campos necesarios
        db_user.nombre = user_info.get('name', db_user.nombre)
        db_user.apellidos = user_info.get('family_name', db_user.apellidos)
        db_user.tipoUsuario = 'Cliente'  # Asignar tipo de usuario "Cliente"
        db_user.estatus = 'Activo'  # Asegurarse de que el estatus sea "Activo"
        db_user.fechaActualizacion = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        # Si el usuario no existe, lo creamos con el tipo de usuario "Cliente"
        db_user = UserModel(
            nombre=user_info.get('name', ''),
            apellidos=user_info.get('family_name', ''),
            tipoUsuario='Cliente',  # Asignar tipo de usuario "Cliente"
            correoElectronico=user_info['email'],
            contrasena=None,  # No se requiere contraseña para Google
            numeroTelefono=user_info.get('phone_number', ''),
            estatus='Activo',  # Asignar estatus "Activo"
            fechaRegistro=datetime.utcnow(),
            fechaActualizacion=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


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
