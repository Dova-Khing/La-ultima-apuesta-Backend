"""
Entidad Partida
===============

Modelo de Partida con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
from sqlalchemy.dialects.postgresql import UUID


from .base import Base


class Partida(Base):
    """
    Modelo de Partida que representa la tabla 'partidas'

    Atributos:
        id (int): Identificador único de la partida
        usuario_id (int): ID del usuario que jugó la partida
        juego_id (int): ID del juego en el que participó
        costo_apuesta (float): Monto de la apuesta
        premio_id (int): ID del premio ganado (nullable si no ganó)
        fecha (datetime): Momento en que se jugó la partida
        estado (str): Estado de la partida ("ganada", "perdida", "en curso")
    """

    __tablename__ = "partidas"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    juego_id = Column(UUID(as_uuid=True), ForeignKey("juegos.id"), nullable=False)
    costo_apuesta: float = Column(Float, nullable=False)
    premio_id = Column(UUID(as_uuid=True), ForeignKey("premios.id"))
    fecha: datetime = Column(DateTime, default=datetime.now, nullable=False)
    estado: str = Column(String(20), nullable=False)

    usuario = relationship("Usuario", back_populates="partidas")
    juego = relationship("Juego", back_populates="partidas")

    def __repr__(self) -> str:
        return (
            f"<Partida(id={self.id}, usuario_id={self.usuario_id}, juego_id={self.juego_id}, "
            f"costo_apuesta={self.costo_apuesta}, estado='{self.estado}')>"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "juego_id": self.juego_id,
            "costo_apuesta": self.costo_apuesta,
            "premio_id": self.premio_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "estado": self.estado,
        }


class PartidaBase(BaseModel):
    """Esquema base para Partida"""

    usuario_id: int = Field(..., description="ID del usuario que juega")
    juego_id: int = Field(..., description="ID del juego en el que participa")
    costo_apuesta: float = Field(..., ge=0, description="Monto de la apuesta")
    premio_id: Optional[int] = Field(
        None, description="ID del premio ganado, si aplica"
    )
    fecha: datetime = Field(
        default_factory=datetime.now, description="Fecha de la partida"
    )
    estado: str = Field(
        ..., description="Estado de la partida (ganada, perdida, en curso)"
    )

    @validator("estado")
    def validar_estado(cls, v: str) -> str:
        estados_validos = {"ganada", "perdida", "en curso"}
        if v.lower() not in estados_validos:
            raise ValueError(f"El estado debe ser uno de: {', '.join(estados_validos)}")
        return v.lower()


class PartidaCreate(PartidaBase):
    """Esquema para crear una nueva partida"""

    pass


class PartidaUpdate(BaseModel):
    """Esquema para actualizar una partida"""

    costo_apuesta: Optional[float] = Field(None, ge=0)
    premio_id: Optional[int] = Field(None)
    estado: Optional[str] = Field(None)

    @validator("estado")
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            estados_validos = {"ganada", "perdida", "en curso"}
            if v.lower() not in estados_validos:
                raise ValueError(
                    f"El estado debe ser uno de: {', '.join(estados_validos)}"
                )
            return v.lower()
        return v


class PartidaResponse(PartidaBase):
    """Esquema para respuesta de partida"""

    id: int

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class PartidaListResponse(BaseModel):
    """Esquema para lista de partidas"""

    partidas: List[PartidaResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True
