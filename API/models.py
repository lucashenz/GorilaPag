from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.types import DECIMAL
from .database import Base
import uuid6
from datetime import datetime

#arquivo que constroi as tabelas do banco de dados, cada class e uma tabela e cada propriendade [e uma coluna]

class Merchant(Base):
    __tablename__ = 'merchants' 

    id = Column( #id e coluna, de string, chave primária, valor automático, Não permite NULL, não existam dois valores iguais
        String, 
        primary_key=True,
        default=lambda: str(uuid6.uuid7()), 
        nullable=False, 
        unique=True
    )

    email = Column (
        String,
        unique=True, 
        index=True, 
        nullable=False
    )

    hashed_password = Column (
        String,
        nullable=False
    )

    callback_url_default = Column(String, nullable=True)

    wallet_address = Column(String, nullable=False)

class PaymentOrder(Base):
    __tablename__ = 'payment_orders' 

    id = Column( 
        String, 
        primary_key=True, 
        default=lambda: str(uuid6.uuid7()), 
        nullable=False, 
        unique=True 
    )

    merchant_id = Column(
        String, 
        ForeignKey("merchants.id"), 
        nullable=False 
    )

    valor = Column( #DOLAR APENAS POR ENQUANTO
        DECIMAL(precision=18, scale=2), 
        nullable=False
    )

    url_callback = Column(
        String,
        nullable=False
    )

    descricao = Column(
        String,
        nullable=True 
    )
    
    status = Column(String, nullable=False, default="pending")
    
    created_at = Column(DateTime, default=datetime.utcnow)