"""
Modulo de autenticacion: hashing de contrasenas, emision/verificacion de JWT
y dependencia de FastAPI que resuelve al usuario autenticado.

Librerias: passlib[bcrypt] + python-jose[cryptography]
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Clave de firma del JWT. En produccion debe venir de una variable de entorno.
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_de_desarrollo_cambiala_en_produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# ---------------------------------------------------------------- contrasenas
def hash_password(password: str) -> str:
    """Hashea una contrasena en texto plano. Devuelve el hash bcrypt ($2b$...)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contrasena en texto plano contra su hash. Nunca lanza excepcion."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


# --------------------------------------------------------------------- tokens
def create_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Crea un JWT firmado con los datos recibidos (típicamente sub y role)."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = dict(data)
    to_encode["exp"] = expire
    to_encode["iat"] = datetime.now(timezone.utc)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------------------------------------------- dependencias
def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Dependencia de FastAPI: extrae el JWT del header Authorization: Bearer <token>,
    lo valida y devuelve el payload del usuario. Si algo falla responde 401.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_error

    username = payload.get("sub")
    if not username:
        raise credentials_error

    return {"sub": username, "role": payload.get("role", "estudiante")}
