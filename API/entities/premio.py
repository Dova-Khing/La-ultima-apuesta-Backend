"""
Entidad Premio
==============

Modelo de Premio con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
from sqlalchemy.dialects.postgresql import UUID


from .base import Base


class Premio(Base):
    """
    Modelo de Premio que representa la tabla 'premios'

    Atributos:
        id (int): Identificador único del premio
        juego_id (int): ID del juego asociado
        descripcion (str): Descripción del premio
        valor (float): Valor económico del premio
        fecha_registro (datetime): Fecha de creación
        fecha_actualizacion (datetime): Fecha de última actualización
        creado_por (str): Usuario que creó el premio
        actualizado_por (str): Último usuario que lo modificó
    """

    __tablename__ = "premios"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    juego_id = Column(UUID(as_uuid=True), ForeignKey("juegos.id"), nullable=False)
    descripcion: str = Column(String(255), nullable=False)
    valor: float = Column(Float, nullable=False, default=0.0)

    fecha_registro: datetime = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion: datetime = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    creado_por: Optional[str] = Column(String(100), nullable=True)
    actualizado_por: Optional[str] = Column(String(100), nullable=True)

    juego = relationship("Juego", backref="premios")

    def __repr__(self) -> str:
        return f"<Premio(id={self.id}, descripcion='{self.descripcion}', valor={self.valor})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "juego_id": self.juego_id,
            "descripcion": self.descripcion,
            "valor": self.valor,
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


class PremioBase(BaseModel):
    """Esquema base para Premio"""

    juego_id: int = Field(..., description="ID del juego asociado")
    descripcion: str = Field(
        ..., min_length=2, max_length=255, description="Descripción del premio"
    )
    valor: float = Field(..., ge=0, description="Valor del premio")

    @validator("descripcion")
    def validar_descripcion(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("La descripción no puede estar vacía")
        return v.strip().capitalize()

    @validator("valor")
    def validar_valor(cls, v: float) -> float:
        if v < 0:
            raise ValueError("El valor no puede ser negativo")
        return v


class PremioCreate(PremioBase):
    """Esquema para crear un nuevo premio"""

    creado_por: Optional[str] = Field(None, description="Usuario que crea el premio")


class PremioUpdate(BaseModel):
    """Esquema para actualizar un premio"""

    descripcion: Optional[str] = Field(None, min_length=2, max_length=255)
    valor: Optional[float] = Field(None, ge=0)
    actualizado_por: Optional[str] = Field(
        None, description="Usuario que actualiza el premio"
    )

    @validator("descripcion")
    def validar_descripcion(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("La descripción no puede estar vacía")
        return v.strip().capitalize() if v else v

    @validator("valor")
    def validar_valor(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("El valor no puede ser negativo")
        return v


class PremioResponse(PremioBase):
    """Esquema para respuesta de premio"""

    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime
    creado_por: Optional[str]
    actualizado_por: Optional[str]

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class PremioListResponse(BaseModel):
    """Esquema para lista de premios"""

    premios: List[PremioResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True
