from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Numeric
from sqlalchemy.types import DECIMAL
from .database import Base
import uuid6
import enum

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


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class PaymentOrder(Base):
    __tablename__ = 'payment_orders' 

    id = Column(String, primary_key=True, index=True)

    merchant_id = Column(String, index=True)

    amount = Column(Numeric(precision=18, scale=8))

    token = Column(String)

    network = Column(String)

    wallet_address = Column(String)

    status = Column(String, default=PaymentStatus.PENDING.value, nullable=False)

    created_at = Column(DateTime)

    expires_at = Column(DateTime)