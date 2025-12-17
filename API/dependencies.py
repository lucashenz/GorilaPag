from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from .security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/merchants/login")

def get_current_merchant(token: str = Depends(oauth2_scheme)): # Ela recebe automaticamente o token JWT do header Authorization: Bearer <token>
    try:
        # Decodifica o JWT usando a chave secreta e o algoritmo configurado
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Isso impede que um refresh token seja usado para acessar rotas protegidas
        if payload.get("type") != "access":
            raise HTTPException(401, "Token inválido.")

        # Recupera o ID do merchant salvo no campo "sub" do token
        merchant_id = payload.get("sub")

        # Se não existir ID no token, ele é considerado inválido
        if not merchant_id:
            raise HTTPException(401, "Token inválido.")

        # Esse valor será injetado na rota que usa Depends(get_current_merchant)
        return merchant_id

    # Caso o token esteja expirado
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expirado.")
    
    except Exception:
        raise HTTPException(401, "Token inválido.")

def erro(mensagem: str, code: int = status.HTTP_400_BAD_REQUEST):
    raise HTTPException(
        status_code=code,
        detail={
            "error": {
                "message": mensagem,
                "type": "request_error",
            }
        }
    )
