"""
Operaciones CRUD para HistorialSaldo
====================================

Este módulo contiene todas las operaciones de base de datos
para la entidad HistorialSaldo.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from ORM.entities.historial_saldo import HistorialSaldo


class HistorialSaldoCRUD:
    """Clase para operaciones CRUD de HistorialSaldo"""

    def __init__(self, db: Session):
        self.db = db

    def crear_movimiento(
        db: Session, usuario_id: int, tipo: str, monto: float
    ) -> HistorialSaldo:
        """
         Crea un nuevo movimiento en el historial de saldo.

        Args:
            usuario_id (int): ID del usuario asociado.
            tipo (str): Tipo de movimiento (ej. 'recarga', 'retiro', 'apuesta').
            monto (float): Valor del movimiento.

        Returns:
            HistorialSaldo: El movimiento creado y persistido en la base de datos.

        """
        movimiento = HistorialSaldo(usuario_id=usuario_id, tipo=tipo, monto=monto)
        db.add(movimiento)
        db.commit()
        db.refresh(movimiento)
        return movimiento

    def obtener_por_id(db: Session, movimiento_id: int) -> Optional[HistorialSaldo]:
        """
         Obtiene un movimiento por su ID.

        Args:
            movimiento_id (int): ID del movimiento a buscar.

        Returns:
            Optional[HistorialSaldo]: El movimiento encontrado o None si no existe.

        """
        return (
            db.query(HistorialSaldo).filter(HistorialSaldo.id == movimiento_id).first()
        )

    def obtener_todos(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[HistorialSaldo]:
        """
         Obtiene una lista de movimientos del historial de saldo.

        Args:
            skip (int, opcional): Número de registros a omitir. Por defecto 0.
            limit (int, opcional): Número máximo de registros a devolver. Por defecto 100.

        Returns:
            List[HistorialSaldo]: Lista de movimientos obtenidos.

        """
        return db.query(HistorialSaldo).offset(skip).limit(limit).all()

    def eliminar_movimiento(db: Session, movimiento_id: int) -> bool:
        movimiento = (
            db.query(HistorialSaldo).filter(HistorialSaldo.id == movimiento_id).first()
        )
        if not movimiento:
            return False
        db.delete(movimiento)
        db.commit()
        return True
