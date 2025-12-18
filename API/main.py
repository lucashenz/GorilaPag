# codigo principal, controla rotas e suas funcionalidades

#-------------------bibliotecas----------------------
from fastapi import FastAPI, Depends, status, Body
from sqlalchemy.orm import Session
from typing import Annotated
import jwt

#-------------------arquivos externos----------------
from . import models
from .database import engine, get_db
from .schemas import dadosCobranca, dadosMerchant, dadosLogin
from .security import (
    SECRET_KEY,
    ALGORITHM,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from .dependencies import get_current_merchant, erro
#------------------------------------------------

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # carrega objeto FastAPI

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # endereço do seu front-end
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine) # carrega e cria banco de dados

db_dependency = Annotated[Session, Depends(get_db)] # Cria um atalho para o FastAPI injetar a sessão do banco nas rotas (get_db)


# ---------------ROTA MERCHANT REGISTER-------------------

@app.post("/v1/merchants/register", status_code=status.HTTP_201_CREATED)

def register_merchant(merchant: dadosMerchant, db: db_dependency): #quando executado recebe dadosMarchant por POST do usuario -> email, senha, wallet e url_padrao

    existing = (db.query(models.Merchant) .filter(models.Merchant.email == merchant.email) .first()) #procura no banco de dados (db) se existe email igual

    if existing: # se existe avisa email ja cadastrado
        erro("Email já cadastrado.", 409) 

    hashed_password = hash_password(merchant.password) # cria um hash para a senha registrada, questao de seguranca

    new_merchant = models.Merchant(         # cria um objeto no modelo de merchant que vai para o banco de dados 
        email=merchant.email,               
        hashed_password=hashed_password,    
        callback_url_default=merchant.callback_url_default,
        wallet_address=merchant.wallet_address
    )

    db.add(new_merchant) #adiciona modelo no banco de dados
    db.commit() #envia
    db.refresh(new_merchant) #atualiza

    return { # essa rota entao retorna ao usuario seu id, email, url_default e wallet address
        "id": new_merchant.id,
        "email": new_merchant.email,
        "callback_url_default": new_merchant.callback_url_default,
        "wallet_address": new_merchant.wallet_address
    }


# --------------ROTA MERCHANT LOGIN-------------------

@app.post("/v1/merchants/login")
def login_merchant( login: dadosLogin, db: db_dependency): #recebe modelo Login-> email, senha e acesso a banco de dados

    merchant = (db.query(models.Merchant).filter(models.Merchant.email == login.email).first()) # verifica se o email esta no banco de dados

    if not merchant: #caso nao esteja 
        erro("Credenciais inválidas.", 401)

    if not verify_password(login.password, merchant.hashed_password): #verfica se o password e o mesmo hash do password 
        erro("Credenciais inválidas.", 401)

    access_token = create_access_token({"sub": merchant.id}) #criar o token de acesso quando logado
    refresh_token = create_refresh_token({"sub": merchant.id}) #crair o refresh do token quando logado

    return { #a rota retorna o token de acesso e o token de refresh e otipo do token - bearer que corresponde a logado
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# --------------REFRESH TOKEN---------------

# Endpoint para renovar o access token usando o refresh token
@app.post("/v1/merchants/refresh")
def refresh_token(refresh_token: str = Body(..., embed=True) ): # Recebe o refresh token 
    try:
        # Decodifica o JWT usando a chave secreta e o algoritmo definido
        # Se o token estiver adulterado ou inválido, gera exceção
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh": # Verifica se o token é realmente do tipo "refresh"
            erro("Token inválido.", 401)

        merchant_id = payload.get("sub") # Extrai o ID do merchant (usuário) salvo no token

        if not merchant_id:  # Garante que o ID existe
            erro("Token inválido.", 401)

    except jwt.ExpiredSignatureError: # Caso o refresh token tenha expirado
        erro("Refresh token expirado.", 401)

    except Exception:
        erro("Token inválido.", 401)

    new_access = create_access_token({"sub": merchant_id}) # Cria um novo access token para o mesmo merchant

    return {  # Retorna o novo token para ser usado nas requisições protegidas
        "access_token": new_access,
        "token_type": "bearer"
    }

# ------------CREATE PAYMENT-------------------

@app.post("/v1/merchants/payments", status_code=status.HTTP_201_CREATED)
def criar_cobranca(cobranca: dadosCobranca, 
                   db: db_dependency, 
                   merchant_id: int = Depends(get_current_merchant)): #recebe modelo de cobranca ->valor, url e descricao + banco de dados + id_merchan por token

    if cobranca.Valor <= 0: #se valor for menor ou igual a 0 aponta erro
        erro("Valor inválido.", 460)

    merchant = db.query(models.Merchant).filter( models.Merchant.id == merchant_id ).first()

    if not merchant_id:  # Garante que o ID existe no banco
            erro("id_marchant invalido", 401)

    if cobranca.URL_callback: #verifica se o campo de url _callback ta preenchido
        
        callback_url = cobranca.URL_callback
    else:
        callback_url = merchant.callback_url_default # se nao usao o url padrao definido no registro

    new_payment = models.PaymentOrder( #cria objeto no modelo de pagamento
        merchant_id=merchant_id,
        valor=cobranca.Valor,
        url_callback=callback_url,
        descricao=cobranca.descricao
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment) # adciona envia e atauliza banco de dados

    return { # retorna o id do pagamento, o valor e o url para pagamento
        "id": new_payment.id,
        "valor_usd": new_payment.valor,
        "payment_url": f"https://gorilapag.com/pay/{new_payment.id}" 
    }
