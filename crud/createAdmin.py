from sqlalchemy.orm import Session
from models.usuarios import User
from passlib.context import CryptContext
from datetime import datetime
from models.usuarios import TipoUsuario, Estatus

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_default_admin(db: Session):
    admin_email = "admin@admin.com"
    admin_password = "admin123"

    existing_admin = db.query(User).filter(User.correoElectronico == admin_email).first()
    if not existing_admin:
        new_admin = User(
            nombre="Admin",
            apellidos="Principal",
            tipoUsuario=TipoUsuario.Administrador,
            correoElectronico=admin_email,
            contrasena=get_password_hash(admin_password),
            numeroTelefono="0000000000",
            estatus=Estatus.Activo,
            fechaRegistro=datetime.utcnow(),
            fechaActualizacion=datetime.utcnow()
        )
        db.add(new_admin)
        db.commit()
        print("✅ Admin creado.")
    else:
        print("🔒 Admin ya existe.")
