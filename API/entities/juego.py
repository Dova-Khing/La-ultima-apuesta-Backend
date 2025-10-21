"""
Entidad Juego
=============

Modelo de Juego con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from .base import Base


class Juego(Base):
    """
    Modelo de Juego que representa la tabla 'juegos'

    Atributos:
        id (int): Identificador único del juego
        nombre (str): Nombre del juego (ej. "Bingo", "Ruleta", "Lotería")
        descripcion (str): Descripción del juego
        costo_base (float): Costo mínimo para jugar
        fecha_registro (datetime): Fecha en la que se creó el juego
        fecha_actualizacion (datetime): Última actualización del juego
        creado_por (str): Usuario/administrador que creó el juego
        actualizado_por (str): Usuario/administrador que actualizó el juego
    """

    __tablename__ = "juegos"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: str = Column(String(100), nullable=False)
    descripcion: Optional[str] = Column(String(255), nullable=True)
    costo_base: float = Column(Float, nullable=False, default=0.0)

    fecha_registro: datetime = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion: datetime = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    creado_por: str = Column(String(100), nullable=False)
    actualizado_por: Optional[str] = Column(String(100), nullable=True)

    partidas = relationship(
        "Partida", back_populates="juego", cascade="all, delete-orphan"
    )
    boletos = relationship(
        "Boleto", back_populates="juego", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Juego(id={self.id}, nombre='{self.nombre}', costo_base={self.costo_base}, "
            f"creado_por='{self.creado_por}', actualizado_por='{self.actualizado_por}')>"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "costo_base": self.costo_base,
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


class JuegoBase(BaseModel):
    """Esquema base para Juego"""

    nombre: str = Field(
        ..., min_length=2, max_length=100, description="Nombre del juego"
    )
    descripcion: Optional[str] = Field(
        None, max_length=255, description="Descripción del juego"
    )
    costo_base: float = Field(..., ge=0, description="Costo mínimo para jugar")
    creado_por: str = Field(
        ..., min_length=2, max_length=100, description="Usuario que creó el juego"
    )
    actualizado_por: Optional[str] = Field(
        None, min_length=2, max_length=100, description="Usuario que actualizó el juego"
    )

    @validator("nombre")
    def validar_nombre(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().title()

    @validator("costo_base")
    def validar_costo(cls, v: float) -> float:
        if v < 0:
            raise ValueError("El costo base no puede ser negativo")
        return v

    @validator("creado_por")
    def validar_creado_por(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El campo 'creado_por' no puede estar vacío")
        return v.strip().title()

    @validator("actualizado_por")
    def validar_actualizado_por(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El campo 'actualizado_por' no puede estar vacío")
        return v.strip().title() if v else v


class JuegoCreate(JuegoBase):
    """Esquema para crear un nuevo juego"""

    pass


class JuegoUpdate(BaseModel):
    """Esquema para actualizar un juego"""

    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    costo_base: Optional[float] = Field(None, ge=0)
    actualizado_por: Optional[str] = Field(None, min_length=2, max_length=100)

    @validator("nombre")
    def validar_nombre(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().title() if v else v

    @validator("costo_base")
    def validar_costo(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("El costo base no puede ser negativo")
        return v

    @validator("actualizado_por")
    def validar_actualizado_por(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El campo 'actualizado_por' no puede estar vacío")
        return v.strip().title() if v else v


class JuegoResponse(JuegoBase):
    """Esquema para respuesta de juego"""

    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class JuegoListResponse(BaseModel):
    """Esquema para lista de juegos"""

    juegos: List[JuegoResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True
