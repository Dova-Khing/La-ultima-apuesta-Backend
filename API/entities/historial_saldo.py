"""
Entidad HistorialSaldo
======================

Modelo de HistorialSaldo con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
from sqlalchemy.dialects.postgresql import UUID


from .base import Base


class HistorialSaldo(Base):
    """
    Modelo de HistorialSaldo que representa la tabla 'historial_saldo'

    Registra cada movimiento de dinero de un usuario.
    """

    __tablename__ = "historial_saldo"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    tipo: str = Column(String(20), nullable=False)  # recarga, apuesta, premio
    monto: float = Column(Float, nullable=False)
    fecha: datetime = Column(DateTime, default=datetime.now, nullable=False)

    usuario = relationship("Usuario", back_populates="historial_saldo")


def __repr__(self) -> str:
    return (
        f"<HistorialSaldo(id={self.id}, usuario_id={self.usuario_id}, "
        f"tipo='{self.tipo}', monto={self.monto}, fecha={self.fecha})>"
    )


def to_dict(self) -> Dict[str, Any]:
    """Convierte el objeto en un diccionario"""
    return {
        "id": self.id,
        "usuario_id": self.usuario_id,
        "tipo": self.tipo,
        "monto": self.monto,
        "fecha": self.fecha.isoformat() if self.fecha else None,
    }


"""
 ESQUEMAS Pydantic
"""


class HistorialSaldoBase(BaseModel):
    """Esquema base de HistorialSaldo"""

    usuario_id: int = Field(..., description="ID del usuario")
    tipo: str = Field(..., description="Tipo de movimiento: recarga, apuesta, premio")
    monto: float = Field(..., gt=0, description="Monto del movimiento")
    fecha: datetime = Field(
        default_factory=datetime.now, description="Fecha del movimiento"
    )

    @validator("tipo")
    def validar_tipo(cls, v: str) -> str:
        tipos_validos = {"recarga", "apuesta", "premio"}
        if v.lower() not in tipos_validos:
            raise ValueError(f"El tipo debe ser uno de: {', '.join(tipos_validos)}")
        return v.lower()


class HistorialSaldoCreate(HistorialSaldoBase):
    """Esquema para crear un nuevo historial de saldo"""

    class Config:
        extra = "forbid"


class HistorialSaldoUpdate(BaseModel):
    """Esquema para actualizar historial de saldo"""

    tipo: Optional[str] = Field(None, description="Tipo de movimiento")
    monto: Optional[float] = Field(None, gt=0)

    @validator("tipo")
    def validar_tipo(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            tipos_validos = {"recarga", "apuesta", "premio"}
            if v.lower() not in tipos_validos:
                raise ValueError(f"El tipo debe ser uno de: {', '.join(tipos_validos)}")
            return v.lower()
        return v


class HistorialSaldoResponse(HistorialSaldoBase):
    """Esquema de respuesta para historial de saldo"""

    id: int

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class HistorialSaldoListResponse(BaseModel):
    """Esquema de lista de historial de saldo"""

    historial: List[HistorialSaldoResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True
