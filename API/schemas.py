from pydantic import BaseModel,Field, model_validator
import re
from decimal import Decimal
from zxcvbn import zxcvbn
from eth_utils import is_checksum_address, to_checksum_address, is_address
from datetime import datetime
from .dependencies import get_current_merchant, erro

#arquivo que constroi as bases dos dados que vai receber do post da rota 
#a biblioteca BaseModel ja pega os dados por base da ordem e do tipo e armazena cada dado na variavel
# eemplo JSON = {"Valor": "50.00", "URL": "ndhddjqdnqj.com", "descricao": "peixes"} -> Valor = 50.00, URL = dnjadb uayd, descricao = peixes.

class dadosCobranca(BaseModel):
    Valor: Decimal
    token_recebido: str
    rede: str
    wallet_recebimento: str
    expires_in: int  

    @model_validator(mode="after")
    def validar_wallet(self):
        addr = self.wallet_recebimento.strip()

        if not is_address(addr):
            erro("Endereço de carteira inválido.", 503)

        # Normalizar checksum
        if not is_checksum_address(addr):
            addr = to_checksum_address(addr)

        self.wallet_recebimento = addr
        return self

class dadosLogin(BaseModel):
    email: str
    password: str

class dadosMerchant(BaseModel):
    email: str
    password: str = Field(..., min_length=12)
    callback_url_default: str | None = None
    wallet_address: str

    @model_validator(mode="after")
    def validar_dados(self):
        
        # Validar força da senha

        score = zxcvbn(self.password)["score"]  # entropia

        if score < 3:
            erro("Senha Fraca", 502)

        # Validar endereço da wallet

        addr = self.wallet_address.strip()

        if not is_address(addr):
            erro("Endereço de carteira inválido.", 503)

        # Normalizar checksum
        if not is_checksum_address(addr):
            addr = to_checksum_address(addr)

        self.wallet_address = addr

        return self
    

    
