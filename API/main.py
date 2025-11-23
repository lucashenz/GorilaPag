from fastapi import FastAPI, Depends, status, Body
from schemas import dadosCobranca, dadosMerchant, dadosLogin
import models
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import Annotated
from . import models, database, schemas, security, dependencies
import jwt
from security import SECRET_KEY, ALGORITHM, validar_url
from dependencies import get_current_merchant, erro

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(database.get_db)]

@app.post('/v1/merchants/register', status_code=status.HTTP_201_CREATED)
def register_merchant(merchant: schemas.dadosMerchant, db: db_dependency):

    existing = db.query(models.Merchant).filter(models.Merchant.email == merchant.email).first()

    if existing:
        dependencies.erro("Email já cadastrado.", 404)
    
    hashed = security.hash_password(merchant.password)

    if merchant.callback_url_default:
        if not validar_url:
            erro("url invalido", 420)

    new_merchant = models.Merchant(
        email = merchant.email,
        hashed_password = hashed,
        callback_url_default = merchant.callback_url_default,
        wallet_address = merchant.wallet_address
    )

    db.add(new_merchant)

    db.commit()
    db.refresh(new_merchant)

    return {
        "id": new_merchant.id,
        "email": new_merchant.email,
        "callback_url_default": new_merchant.callback_url_default,
        "wallet_address": new_merchant.wallet_address
    }

@app.post('/v1/merchants/login', status_code=status.HTTP_201_CREATED)
def login_merchant(login: dadosLogin, db: db_dependency):

    merchant = db.query(models.Merchant).filter(models.Merchant.email == login.email).first()

    if not merchant:
        dependencies.erro("acesso invalido", 401)
    
    if not security.verify_password(login.password, merchant.hashed_password):
        dependencies.erro("acesso invalido", 401)

    access = security.create_access_token({"sub": merchant.id})
    refresh = security.create_refresh_token({"sub": merchant.id})

    return {
        "access_token": access,
        "token_type": "bearer"
    }

@app.post("/v1/merchants/refresh")
def refresh_token(refresh_token: str = Body(..., embed=True)):

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            dependencies.erro("Token inválido")

        merchant_id = payload.get("sub")

    except jwt.ExpiredSignatureError:
        dependencies.erro("Refresh token expirado.")

    except Exception:
        dependencies.erro("Token inválido.")

    new_access = security.create_access_token({"sub": merchant_id})

    return {"access_token": new_access}
    
@app.post('/v1/merchants/payments', status_code=status.HTTP_201_CREATED)
def cobranca(
    cobranca: dadosCobranca,
    db: db_dependency,
    merchant_id = Depends(get_current_merchant)
):

    if cobranca.Valor <= 0:
        erro("Valor inválido", 460)

    callback_url = cobranca.callback_url_default
    if callback_url:
        if not validar_url(callback_url):
            erro("URL inválida", 420)

    new_cobranca = models.PaymentOrder(
        client_id=merchant_id,
        valor=cobranca.Valor,
        url_callback=callback_url,
        descricao=cobranca.descricao
    )

    db.add(new_cobranca)
    db.commit()
    db.refresh(new_cobranca)

    # gerar link
    payment_url = f"https://gorilapag.com/pay/{new_cobranca.id}"

    # endereço do contrato (fixo ou config)
    SMART_CONTRACT = "0xAbC123...890"  # exemplo

    return {
        "id": new_cobranca.id,
        "valor_usd": new_cobranca.valor,
        "contract_address": SMART_CONTRACT,
        "payment_url": payment_url
    }

       

