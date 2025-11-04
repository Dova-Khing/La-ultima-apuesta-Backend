"""
Modelos Pydantic para las respuestas de la API
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


# Modelos base para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None
    edad: str
    saldo_inicial: int
    es_admin: bool = False


class UsuarioCreate(UsuarioBase):
    contrasena: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    edad: Optional[str] = None
    saldo_inicial: Optional[int] = None
    es_admin: Optional[bool] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: UUID
    activo: bool
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str


class CambioContrasena(BaseModel):
    contrasena_actual: str
    nueva_contrasena: str


# Modelos base para Premio
class PremioBase(BaseModel):
    descripcion: str
    valor: float


class PremioCreate(PremioBase):
    juego_id: UUID
    creado_por: Optional[str] = None


class PremioUpdate(BaseModel):
    descripcion: Optional[str] = None
    valor: Optional[float] = None
    juego_id: Optional[UUID] = None
    actualizado_por: Optional[str] = None


class PremioResponse(PremioBase):
    id: UUID
    juego_id: UUID
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    creado_por: Optional[str] = None
    actualizado_por: Optional[str] = None

    class Config:
        from_attributes = True


# Modelos base para Partida
class PartidaBase(BaseModel):
    costo_apuesta: float
    estado: str


class PartidaCreate(PartidaBase):
    usuario_id: UUID
    juego_id: UUID
    premio_id: Optional[UUID] = None


class PartidaUpdate(BaseModel):
    costo_apuesta: Optional[float] = None
    estado: Optional[str] = None
    usuario_id: Optional[UUID] = None
    juego_id: Optional[UUID] = None
    premio_id: Optional[UUID] = None


class PartidaResponse(PartidaBase):
    id: UUID
    usuario_id: UUID
    juego_id: UUID
    premio_id: Optional[UUID] = None
    fecha: datetime

    class Config:
        from_attributes = True


# Modelos base para Juego
class JuegoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    costo_base: float


class JuegoCreate(JuegoBase):
    creado_por: str


class JuegoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    costo_base: Optional[float] = None
    creado_por: Optional[str] = None
    actualizado_por: Optional[str] = None


class JuegoResponse(JuegoBase):
    id: UUID
    fecha_registro: datetime
    fecha_actualizacion: datetime
    creado_por: str
    actualizado_por: Optional[str] = None

    class Config:
        from_attributes = True


# Modelos base para HistorialSaldo
class HistorialSaldoBase(BaseModel):
    tipo: str  # recarga, apuesta, premio
    monto: float


class HistorialSaldoCreate(HistorialSaldoBase):
    usuario_id: UUID


class HistorialSaldoUpdate(BaseModel):
    tipo: Optional[str] = None
    monto: Optional[float] = None
    usuario_id: Optional[UUID] = None


class HistorialSaldoResponse(HistorialSaldoBase):
    id: UUID
    usuario_id: UUID
    fecha: datetime

    class Config:
        from_attributes = True


# Modelos base para Boleto
class BoletoBase(BaseModel):
    numeros: str
    costo: float


class BoletoCreate(BoletoBase):
    usuario_id: UUID
    juego_id: UUID
    creado_por: str


class BoletoUpdate(BaseModel):
    numeros: Optional[str] = None
    costo: Optional[float] = None
    usuario_id: Optional[UUID] = None
    juego_id: Optional[UUID] = None
    actualizado_por: Optional[str] = None


class BoletoResponse(BoletoBase):
    id: UUID
    usuario_id: UUID
    juego_id: UUID
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    creado_por: str
    actualizado_por: Optional[str] = None

    class Config:
        from_attributes = True


# Modelos de respuesta con relaciones
class UsuarioConPartidas(UsuarioResponse):
    partidas: list[PartidaResponse] = []


class UsuarioConBoletos(UsuarioResponse):
    boletos: list[BoletoResponse] = []


class UsuarioConHistorialSaldo(UsuarioResponse):
    historial_saldo: list[HistorialSaldoResponse] = []


class PremioConJuego(PremioResponse):
    juego: JuegoResponse


class PartidaConUsuario(PartidaResponse):
    usuario: UsuarioResponse


class PartidaConJuego(PartidaResponse):
    juego: JuegoResponse


class JuegoConPartidas(JuegoResponse):
    partidas: list[PartidaResponse] = []


class JuegoConBoletos(JuegoResponse):
    boletos: list[BoletoResponse] = []


class HistorialSaldoConUsuario(HistorialSaldoResponse):
    usuario: UsuarioResponse


# Boleto con relaciones
class BoletoConUsuario(BoletoResponse):
    usuario: UsuarioResponse


class BoletoConJuego(BoletoResponse):
    juego: JuegoResponse


# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
