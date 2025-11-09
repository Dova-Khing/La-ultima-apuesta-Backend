"""
Operaciones CRUD para HistorialSaldo
====================================

Este módulo contiene todas las operaciones de base de datos
para la entidad HistorialSaldo.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID


from entities.historial_saldo import HistorialSaldo


class HistorialSaldoCRUD:
    """Clase para operaciones CRUD de HistorialSaldo"""

    def __init__(self, db: Session):
        """Inicializa la clase con la sesión de base de datos."""
        self.db = db

    def crear_movimiento(
        self, usuario_id: UUID, tipo: str, monto: float
    ) -> HistorialSaldo:
        """
        Crea un nuevo movimiento en el historial de saldo.

        Args:
            usuario_id (UUID): ID del usuario asociado (Corregido a UUID).
            tipo (str): Tipo de movimiento (ej. 'recarga', 'apuesta', 'premio').
            monto (float): Valor del movimiento.

        Returns:
            HistorialSaldo: El movimiento creado y persistido en la base de datos.
        """
        movimiento = HistorialSaldo(usuario_id=usuario_id, tipo=tipo, monto=monto)
        self.db.add(movimiento)
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento

    def obtener_por_id(self, movimiento_id: UUID) -> Optional[HistorialSaldo]:
        """
        Obtiene un movimiento por su ID (Corregido a UUID).

        Args:
            movimiento_id (UUID): ID del movimiento a buscar.

        Returns:
            Optional[HistorialSaldo]: El movimiento encontrado o None si no existe.
        """
        return (
            self.db.query(HistorialSaldo)
            .filter(HistorialSaldo.id == movimiento_id)
            .first()
        )

    def obtener_todos(
        self, usuario_id: Optional[UUID] = None, skip: int = 0, limit: int = 100
    ) -> List[HistorialSaldo]:
        """
        Obtiene una lista de movimientos del historial de saldo con paginación
        y filtro opcional por usuario.

        Args:
            usuario_id (Optional[UUID]): Filtra movimientos de un usuario específico.
            skip (int, opcional): Número de registros a omitir.
            limit (int, opcional): Número máximo de registros a devolver.

        Returns:
            List[HistorialSaldo]: Lista de movimientos obtenidos.
        """
        query = self.db.query(HistorialSaldo)

        if usuario_id:
            query = query.filter(HistorialSaldo.usuario_id == usuario_id)

        return query.offset(skip).limit(limit).all()

    def eliminar_movimiento(self, movimiento_id: UUID) -> bool:
        """
        Elimina un movimiento por su ID (Corregido a UUID).
        """
        movimiento = self.obtener_por_id(movimiento_id)

        if not movimiento:
            return False

        self.db.delete(movimiento)
        self.db.commit()
        return True
