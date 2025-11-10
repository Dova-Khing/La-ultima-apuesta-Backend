"""
Operaciones CRUD para Partida
=============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Partida.
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from entities.partida import Partida
from uuid import UUID


class PartidaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_partida(
        self,
        usuario_id: UUID,
        juego_id: UUID,
        costo_apuesta: float,
        estado: str,
        premio_id: Optional[UUID] = None,
    ):
        """
        Crea una nueva partida en la base de datos.

        Args:
            usuario_id (UUID): ID del usuario que juega.
            juego_id (UUID): ID del juego.
            costo_apuesta (float): Monto de la apuesta.
            estado (str): Estado inicial de la partida.
            premio_id (Optional[UUID]): ID del premio asociado, si existe.

        Returns:
            Partida: Objeto Partida creado y persistido en la base de datos
        """
        partida = Partida(
            usuario_id=usuario_id,
            juego_id=juego_id,
            costo_apuesta=costo_apuesta,
            estado=estado,
            premio_id=premio_id,
        )
        self.db.add(partida)
        self.db.commit()
        self.db.refresh(partida)
        return partida

    def obtener_por_id(self, partida_id: UUID) -> Optional[Partida]:
        """
        Obtiene una partida por su ID.

        Args:
            partida_id (UUID): ID de la partida.

        Returns:
            Optional[Partida]: Instancia de la partida o None si no existe.
        """
        return self.db.query(Partida).filter(Partida.id == partida_id).first()

    def obtener_partidas(self, skip: int = 0, limit: int = 100) -> List[Partida]:
        """
        Obtiene todas las partidas con paginación opcional.

        Args:
            skip (int): Número de registros a saltar.
            limit (int): Número máximo de registros a retornar.

        Returns:
            List[Partida]: Lista de partidas.
        """
        return self.db.query(Partida).offset(skip).limit(limit).all()

    def actualizar_partida(
        self,
        partida_id: UUID,
        partida_data: Dict[str, Any],
    ) -> Optional[Partida]:
        """
        Actualiza los campos de una partida.

        Args:
            partida_id (UUID): ID de la partida a actualizar.
            partida_data (Dict[str, Any]): Diccionario con los datos a actualizar.

        Returns:
            Optional[Partida]: Instancia actualizada de la partida o None si no existe.
        """
        partida = self.db.query(Partida).filter(Partida.id == partida_id).first()
        if not partida:
            return None

        # Actualiza dinámicamente los campos
        for key, value in partida_data.items():
            if value is not None:
                setattr(partida, key, value)

        self.db.commit()
        self.db.refresh(partida)
        return partida

    def eliminar_partida(self, partida_id: UUID) -> bool:
        """
        Elimina una partida por su ID.

        Args:
            partida_id (UUID): ID de la partida a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existe.
        """
        partida = self.db.query(Partida).filter(Partida.id == partida_id).first()
        if not partida:
            return False
        self.db.delete(partida)
        self.db.commit()
        return True
