"""
Entidad Usuario
===============

Modelo de Usuario con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


from .base import Base


class Usuario(Base):
    """
    Modelo de Usuario que representa la tabla 'usuarios'

    Atributos:
        id: Identificador único
        nombre: Nombre completo
        edad: Edad del usuario
        saldo_inicial: Saldo actual
        nombre_usuario: Nombre único para login
        email: Correo electrónico único
        contrasena_hash: Hash de la contraseña
        telefono: Número telefónico
        activo: Estado activo/inactivo
        es_admin: Si el usuario tiene permisos de administrador
        fecha_registro: Fecha de creación
        fecha_actualizacion: Última actualización
    """

    __tablename__ = "usuarios"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: str = Column(String(100), nullable=False)
    nombre_usuario: str = Column(String(50), unique=True, index=True, nullable=False)
    email: str = Column(String(150), unique=True, index=True, nullable=False)
    telefono: Optional[str] = Column(String(20), nullable=True)
    contrasena_hash: str = Column(String(255), nullable=False)
    edad: str = Column(String(3), nullable=False)
    saldo_inicial: int = Column(Integer, nullable=False, default=0)
    activo: bool = Column(Boolean, default=True)
    es_admin: bool = Column(Boolean, default=False)

    fecha_registro: datetime = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion: datetime = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    partidas = relationship(
        "Partida", back_populates="usuario", cascade="all, delete-orphan"
    )
    boletos = relationship(
        "Boleto", back_populates="usuario", cascade="all, delete-orphan"
    )
    historial_saldo = relationship(
        "HistorialSaldo", back_populates="usuario", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, usuario='{self.nombre_usuario}', email='{self.email}')>"

    def to_dict(self) -> dict[str, any]:
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "saldo_inicial": self.saldo_inicial,
            "nombre_usuario": self.nombre_usuario,
            "email": self.email,
            "telefono": self.telefono,
            "activo": self.activo,
            "es_admin": self.es_admin,
            "fecha_registro": (
                self.fecha_registro.isoformat() if self.fecha_registro else None
            ),
            "fecha_actualizacion": (
                self.fecha_actualizacion.isoformat()
                if self.fecha_actualizacion
                else None
            ),
        }


"""
ESQUEMAS DE PYDANTIC
"""


class UsuarioBase(BaseModel):
    """Esquema base para Usuario"""

    nombre: str = Field(
        ..., min_length=2, max_length=100, description="Nombre completo"
    )
    edad: str = Field(..., min_length=1, max_length=3, description="Edad")
    saldo_inicial: int = Field(..., ge=0, description="Saldo inicial")

    nombre_usuario: str = Field(
        ..., min_length=3, max_length=50, description="Nombre de usuario único"
    )
    email: EmailStr = Field(..., description="Correo electrónico único")
    telefono: Optional[str] = Field(
        None, max_length=20, description="Número de teléfono"
    )
    activo: bool = Field(True, description="Estado activo/inactivo")
    es_admin: bool = Field(False, description="¿Es administrador?")

    @validator("nombre")
    def validar_nombre(cls, v) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().title()

    @validator("edad")
    def validar_edad(cls, v) -> str:
        if not v.isdigit():
            raise ValueError("La edad debe ser numérica")
        return v

    @validator("saldo_inicial")
    def validar_saldo(cls, v) -> int:
        if v < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        return v


class UsuarioCreate(UsuarioBase):
    """Esquema para crear un nuevo usuario"""

    contrasena: str = Field(
        ..., min_length=6, description="Contraseña en texto plano (será hasheada)"
    )


class UsuarioUpdate(BaseModel):
    """Esquema para actualizar un usuario"""

    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    edad: Optional[str] = Field(None, min_length=1, max_length=3)
    saldo_inicial: Optional[int] = Field(None, ge=0)

    nombre_usuario: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None
    es_admin: Optional[bool] = None
    contrasena: Optional[str] = Field(None, min_length=6)

    @validator("nombre")
    def validar_nombre(cls, v) -> str:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().title() if v else v

    @validator("edad")
    def validar_edad(cls, v) -> str:
        if v is not None and not v.isdigit():
            raise ValueError("La edad debe ser numérica")
        return v

    @validator("saldo_inicial")
    def validar_saldo(cls, v) -> int:
        if v is not None and v < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        return v


class UsuarioResponse(UsuarioBase):
    """Esquema para respuesta de usuario"""

    id: uuid.UUID
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class UsuarioListResponse(BaseModel):
    """Esquema para lista de usuarios"""

    usuarios: List[UsuarioResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True
