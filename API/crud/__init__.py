"""
Módulo de operaciones CRUD
==========================

Este módulo centraliza todas las operaciones CRUD
(Create, Read, Update, Delete) de las entidades del sistema.
"""

from .usuario_crud import UsuarioCRUD
from .juego_crud import JuegoCRUD
from .partida_crud import PartidaCRUD
from .historial_saldo_crud import HistorialSaldoCRUD
from .Boleto_crud import BoletoCRUD
from .premio_crud import PremioCRUD

__all__ = [
    "UsuarioCRUD",
    "JuegoCRUD",
    "PartidaCRUD",
    "HistorialSaldoCRUD",
    "BoletoCRUD",
    "PremioCRUD",
]
