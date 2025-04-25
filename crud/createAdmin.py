from sqlalchemy.orm import Session
from models.usuarios import User
from passlib.context import CryptContext
from datetime import datetime
from models.usuarios import TipoUsuario, Estatus

# Contexto de passlib con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear contraseñas
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Crear un admin por defecto
def create_default_admin(db: Session):
    admin_email = "admin@admin.com"
    admin_password = "admin123"

    # Verificar si el admin ya existe
    existing_admin = db.query(User).filter(User.correoElectronico == admin_email).first()
    if not existing_admin:
        # Crear el nuevo admin
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
