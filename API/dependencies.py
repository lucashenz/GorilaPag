from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from .security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/merchants/login")

def get_current_merchant(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(401, "Token inválido.")

        merchant_id = payload.get("sub")

        if not merchant_id:
            raise HTTPException(401, "Token inválido.")

        return merchant_id

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
