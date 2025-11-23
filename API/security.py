import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from urllib.parse import urlparse

SECRET_KEY = "senha"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode["exp"] = expire
    to_encode["type"] = "access"

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode["exp"] = expire
    to_encode["type"] = "refresh"

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


pwd_context = CryptContext(
    schemes=["argon2"],
    default="argon2",
    argon2__memory_cost=65536,   # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=1
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def validar_url(url: str) -> bool:
    try:
        resultado = urlparse(url)
        return all([resultado.scheme in ["http", "https"], resultado.netloc])
    except:
        return False
