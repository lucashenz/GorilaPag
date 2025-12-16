from fastapi import FastAPI, Depends, status, Body
from sqlalchemy.orm import Session
from typing import Annotated
import jwt

from . import models
from .database import engine, get_db
from .schemas import dadosCobranca, dadosMerchant, dadosLogin
from .security import (
    SECRET_KEY,
    ALGORITHM,
    validar_url,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from .dependencies import get_current_merchant, erro


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

# MERCHANT REGISTER

@app.post("/v1/merchants/register", status_code=status.HTTP_201_CREATED)
def register_merchant(
    merchant: dadosMerchant,
    db: db_dependency
):
    existing = (
        db.query(models.Merchant)
        .filter(models.Merchant.email == merchant.email)
        .first()
    )

    if existing:
        erro("Email já cadastrado.", 409)

    if merchant.callback_url_default:
        if not validar_url(merchant.callback_url_default):
            erro("URL inválida.", 420)

    hashed_password = hash_password(merchant.password)

    new_merchant = models.Merchant(
        email=merchant.email,
        hashed_password=hashed_password,
        callback_url_default=merchant.callback_url_default,
        wallet_address=merchant.wallet_address
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


# MERCHANT LOGIN

@app.post("/v1/merchants/login")
def login_merchant(
    login: dadosLogin,
    db: db_dependency
):
    merchant = (
        db.query(models.Merchant)
        .filter(models.Merchant.email == login.email)
        .first()
    )

    if not merchant:
        erro("Credenciais inválidas.", 401)

    if not verify_password(login.password, merchant.hashed_password):
        erro("Credenciais inválidas.", 401)

    access_token = create_access_token({"sub": merchant.id})
    refresh_token = create_refresh_token({"sub": merchant.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# REFRESH TOKEN

@app.post("/v1/merchants/refresh")
def refresh_token(refresh_token: str = Body(..., embed=True)):
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            erro("Token inválido.", 401)

        merchant_id = payload.get("sub")

    except jwt.ExpiredSignatureError:
        erro("Refresh token expirado.", 401)

    except Exception:
        erro("Token inválido.", 401)

    new_access = create_access_token({"sub": merchant_id})

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }

# CREATE PAYMENT

@app.post("/v1/merchants/payments", status_code=status.HTTP_201_CREATED)
def criar_cobranca(
    cobranca: dadosCobranca,
    db: db_dependency,
    merchant_id: int = Depends(get_current_merchant)
):
    if cobranca.valor <= 0:
        erro("Valor inválido.", 460)

    callback_url = cobranca.callback_url_default
    if callback_url:
        if not validar_url(callback_url):
            erro("URL inválida.", 420)

    new_payment = models.PaymentOrder(
        client_id=merchant_id,
        valor=cobranca.valor,
        url_callback=callback_url,
        descricao=cobranca.descricao
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    payment_url = f"https://gorilapag.com/pay/{new_payment.id}"

    SMART_CONTRACT = "0xAbC123...890"

    return {
        "id": new_payment.id,
        "valor_usd": new_payment.valor,
        "contract_address": SMART_CONTRACT,
        "payment_url": payment_url
    }
