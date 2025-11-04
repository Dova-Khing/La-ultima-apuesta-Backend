"""
Operaciones CRUD para Partida
=============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Partida.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from ORM.entities.partida import Partida


class PartidaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_partida(
        self,
        usuario_id: int,
        juego_id: int,
        costo_apuesta: float,
        estado: str,
        premio_id: Optional[int] = None,
    ):
        """
        Crea una nueva partida en la base de datos.

         Args:
             usuario_id (int): ID del usuario que juega.
             juego_id (int): ID del juego.
             costo_apuesta (float): Monto de la apuesta.
             estado (str): Estado inicial de la partida.
             premio_id (Optional[int]): ID del premio asociado, si existe.

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

    def obtener_por_id(db: Session, partida_id: int) -> Optional[Partida]:
        """
        Obtiene una partida por su ID.

        Args:
            db (Session): Sesión de base de datos.
            partida_id (int): ID de la partida.

        Returns:
            Optional[Partida]: Instancia de la partida o None si no existe.


        """
        return db.query(Partida).filter(Partida.id == partida_id).first()

    def obtener_todas(db: Session, skip: int = 0, limit: int = 100) -> List[Partida]:
        """

        Obtiene todas las partidas con paginación opcional.

        Args:
            db (Session): Sesión de base de datos.
            skip (int): Número de registros a saltar.
            limit (int): Número máximo de registros a retornar.

        Returns:
            List[Partida]: Lista de partidas.


        """
        return db.query(Partida).offset(skip).limit(limit).all()

    def actualizar_partida(
        db: Session,
        partida_id: int,
        estado: Optional[str] = None,
        premio_id: Optional[int] = None,
    ) -> Optional[Partida]:
        """
        Actualiza el estado o el premio de una partida.

        Args:
            db (Session): Sesión de base de datos.
            partida_id (int): ID de la partida a actualizar.
            estado (Optional[str]): Nuevo estado de la partida.
            premio_id (Optional[int]): Nuevo ID de premio asociado.

        Returns:
            Optional[Partida]: Instancia actualizada de la partida o None si no existe.


        """
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not partida:
            return None

        if estado is not None:
            partida.estado = estado
        if premio_id is not None:
            partida.premio_id = premio_id

        db.commit()
        db.refresh(partida)
        return partida

    def eliminar_partida(db: Session, partida_id: int) -> bool:
        """
        Elimina una partida por su ID.

        Args:
            db (Session): Sesión de base de datos.
            partida_id (int): ID de la partida a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existe.

        """
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not partida:
            return False
        db.delete(partida)
        db.commit()
        return True
