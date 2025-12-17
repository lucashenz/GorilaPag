import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from urllib.parse import urlparse

#serve para cuidar da seguranca do site e login, por meio do Token JWT onde cada usuario logado recebe ele para poder entrar nas rotas

SECRET_KEY = "senha"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #atualiza o token em 30 e 30 minutos
REFRESH_TOKEN_EXPIRE_DAYS = 7 # expira em 7 dias o aceso ao site

# Cria um token JWT de acesso (curta duração)
def create_access_token(data: dict, expires_delta: int = None):
    # Copia os dados para não alterar o original
    to_encode = data.copy()

    # Define a data de expiração (minutos)
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Adiciona expiração ao token
    to_encode["exp"] = expire

    # Marca o tipo do token como access
    to_encode["type"] = "access"

    # Gera e retorna o JWT assinado
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Cria um token JWT de refresh (longa duração)
def create_refresh_token(data: dict):
    # Copia os dados
    to_encode = data.copy()

    # Define expiração em dias
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # Adiciona expiração
    to_encode["exp"] = expire

    # Marca o tipo do token como refresh
    to_encode["type"] = "refresh"

    # Gera e retorna o JWT assinado
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Configuração do algoritmo de hash de senha (Argon2)
pwd_context = CryptContext(
    schemes=["argon2"],          # Algoritmo usado
    default="argon2",
    argon2__memory_cost=65536,   # Memória usada (64 MB)
    argon2__time_cost=3,         # Iterações
    argon2__parallelism=1        # Threads
)


# Gera o hash seguro da senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verifica se a senha bate com o hash salvo
def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# Valida se uma URL é válida (http ou https)
def validar_url(url: str) -> bool:
    try:
        resultado = urlparse(url)
        # Verifica esquema e domínio
        return all([
            resultado.scheme in ["http", "https"],
            resultado.netloc
        ])
    except:
        return False