from models.usuarios import User as UserModel
from schemas.usuarios import UserCreate, UserUpdate
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
# Obtener un usuario por correo electrónico
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.correoElectronico == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

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

# Crear o actualizar un usuario con OAuth de Google
def create_or_update_user_with_google(db: Session, user_info: dict):
    # Buscar el usuario por el correo electrónico
    existing_user = get_user_by_email(db, user_info["email"])
    
    if existing_user:
        # Si el usuario ya existe, actualizamos los datos
        existing_user.nombre = user_info["given_name"]
        existing_user.apellidos = user_info["family_name"]
        existing_user.fechaActualizacion = datetime.utcnow()
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        # Si el usuario no existe, lo creamos
        user_create = UserCreate(
            nombre=user_info["given_name"],
            apellidos=user_info["family_name"],
            correoElectronico=user_info["email"],
            tipoUsuario="Cliente",  # O "Administrador" si corresponde
            nombreUsuario=user_info["email"],  # Usamos el correo como nombre de usuario
            contrasena="randomPassword123",  # Asigna una contraseña temporal aquí
            numeroTelefono=None,  # Este dato puede no estar disponible en Google OAuth
            estatus="Activo"  # Por defecto, activo
        )
        return create_user(db, user_create)

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
