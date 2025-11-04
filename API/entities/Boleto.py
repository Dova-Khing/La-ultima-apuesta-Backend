"""
Entidad Boleto
==============

Modelo de Boleto con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Boleto(Base):
    """
    Modelo de Boleto que representa la tabla 'boletos'

    Aplica a juegos que usan boletos (ejemplo: Bingo, Lotería).
    """

    __tablename__ = "boletos"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    juego_id = Column(UUID(as_uuid=True), ForeignKey("juegos.id"), nullable=False)
    numeros: str = Column(String(255), nullable=False)  # Ejemplo: "5,10,23,45"
    costo: float = Column(Float, nullable=False)

    fecha_registro: datetime = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion: datetime = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    creado_por: str = Column(String(100), nullable=False)
    actualizado_por: Optional[str] = Column(String(100), nullable=True)

    usuario = relationship("Usuario", back_populates="boletos")
    juego = relationship("Juego", back_populates="boletos")

    def __repr__(self) -> str:
        return (
            f"<Boleto(id={self.id}, usuario_id={self.usuario_id}, juego_id={self.juego_id}, "
            f"costo={self.costo}, fecha_registro={self.fecha_registro})>"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto en un diccionario"""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "juego_id": self.juego_id,
            "numeros": self.numeros,
            "costo": self.costo,
            "fecha_registro": (
                self.fecha_registro.isoformat() if self.fecha_registro else None
            ),
            "fecha_actualizacion": (
                self.fecha_actualizacion.isoformat()
                if self.fecha_actualizacion
                else None
            ),
            "creado_por": self.creado_por,
            "actualizado_por": self.actualizado_por,
        }


"""
Esquemas de pydantic para validacion
"""


class BoletoBase(BaseModel):
    """Esquema base de Boleto"""

    usuario_id: int = Field(..., description="ID del usuario que compra el boleto")
    juego_id: int = Field(..., description="ID del juego asociado al boleto")
    numeros: str = Field(..., description="Números del boleto en formato '5,10,23,45'")
    costo: float = Field(..., gt=0, description="Costo del boleto")

    @validator("numeros")
    def validar_numeros(cls, v: str) -> str:
        """Valida que los números sean enteros separados por comas"""
        numeros = [x.strip() for x in v.split(",")]
        if not all(n.isdigit() for n in numeros):
            raise ValueError(
                "Todos los valores en 'numeros' deben ser enteros separados por comas"
            )
        return ",".join(numeros)


class BoletoCreate(BoletoBase):
    """Esquema para crear un boleto"""

    creado_por: str = Field(
        ..., min_length=2, max_length=100, description="Usuario que crea el boleto"
    )


class BoletoResponse(BoletoBase):
    """Esquema de respuesta para boleto"""

    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime]
    creado_por: str
    actualizado_por: Optional[str]

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class BoletoListResponse(BaseModel):
    """Esquema para lista de boletos"""

    boletos: List[BoletoResponse]
    total: int
    pagina: int
    por_pagina: int


class Config:
    from_attributes = True


class BoletoUpdate(BaseModel):
    """Esquema para actualizar un boleto"""

    numeros: Optional[str] = Field(
        None, description="Nuevos números del boleto en formato '5,10,23,45'"
    )
    costo: Optional[float] = Field(None, gt=0, description="Nuevo costo del boleto")
    actualizado_por: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Usuario que actualiza el boleto",
    )

    @validator("numeros")
    def validar_numeros(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        numeros = [x.strip() for x in v.split(",")]
        if not all(n.isdigit() for n in numeros):
            raise ValueError(
                "Todos los valores en 'numeros' deben ser enteros separados por comas"
            )
        return ",".join(numeros)
