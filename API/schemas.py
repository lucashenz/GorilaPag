from pydantic import BaseModel,Field, model_validator
import re
from decimal import Decimal
from zxcvbn import zxcvbn
from eth_utils import is_checksum_address, to_checksum_address, is_address

#arquivo que constroi as bases dos dados que vai receber do post da rota 
#a biblioteca BaseModel ja pega os dados por base da ordem e do tipo e armazena cada dado na variavel
# eemplo JSON = {"Valor": "50.00", "URL": "ndhddjqdnqj.com", "descricao": "peixes"} -> Valor = 50.00, URL = dnjadb uayd, descricao = peixes.

class dadosCobranca(BaseModel):
    Valor: Decimal
    URL_callback: str
    descricao: str

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
            raise ValueError("Senha fraca. Aumente a complexidade.")

        # Validar endereço da wallet

        addr = self.wallet_address.strip()

        if not is_address(addr):
            raise ValueError("Endereço de carteira inválido.")

        # Normalizar checksum
        if not is_checksum_address(addr):
            addr = to_checksum_address(addr)

        self.wallet_address = addr

        return self
    

    
