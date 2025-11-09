"""
Operaciones CRUD para Juego
===========================

Este módulo contiene todas las operaciones de base de datos
para la entidad Juego.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from entities.juego import Juego
from entities.premio import Premio
from entities.partida import Partida
from entities.Boleto import Boleto
from uuid import UUID


class JuegoCRUD:
    """Clase para operaciones CRUD de Juego"""

    def __init__(self, db: Session):
        self.db = db

    def crear_juego(
        self,
        nombre: str,
        descripcion: Optional[str],
        costo_base: float,
        creado_por: Optional[str] = None,
    ) -> Juego:
        """
        Crea un nuevo juego en la base de datos.
        """
        juego = Juego(
            nombre=nombre,
            descripcion=descripcion,
            costo_base=costo_base,
            creado_por=creado_por,
        )
        self.db.add(juego)
        self.db.commit()
        self.db.refresh(juego)
        return juego

    def obtener_juegos(self, skip: int = 0, limit: int = 100) -> List[Juego]:
        """
        Obtiene todos los juegos, con soporte para paginación.
        """
        return self.db.query(Juego).offset(skip).limit(limit).all()

    def obtener_por_id(self, juego_id: UUID) -> Optional[Juego]:
        """Obtiene un juego por su ID."""
        return self.db.query(Juego).filter(Juego.id == juego_id).first()

    def obtener_juego(self, juego_id: UUID) -> Optional[Juego]:
        return self.obtener_por_id(juego_id)

    def actualizar_juego(
        self,
        juego_id: UUID,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        costo_base: Optional[float] = None,
        actualizado_por: Optional[str] = None,
    ) -> Optional[Juego]:
        """Actualiza un juego existente por su ID."""
        juego = self.db.query(Juego).filter(Juego.id == juego_id).first()
        if not juego:
            return None

        if nombre is not None:
            juego.nombre = nombre
        if descripcion is not None:
            juego.descripcion = descripcion
        if costo_base is not None:
            juego.costo_base = costo_base
        if actualizado_por is not None:
            juego.actualizado_por = actualizado_por

        self.db.commit()
        self.db.refresh(juego)
        return juego

    def eliminar_juego(self, juego_id: UUID) -> bool:
        """Elimina un juego por su ID."""
        juego = self.db.query(Juego).filter(Juego.id == juego_id).first()
        if not juego:
            return False

        relacionado = (
            self.db.query(Premio).filter(Premio.juego_id == juego_id).first()
            or self.db.query(Partida).filter(Partida.juego_id == juego_id).first()
            or self.db.query(Boleto).filter(Boleto.juego_id == juego_id).first()
        )

        if relacionado:
            return False

        self.db.delete(juego)
        self.db.commit()
        return True
