"""
Operaciones CRUD para Premio
============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Premio.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from entities.premio import Premio
from uuid import UUID
from sqlalchemy.exc import IntegrityError


class PremioCRUD:
    """Clase para operaciones CRUD de Premio"""

    def __init__(self, db: Session):
        """Inicializa la clase con la sesión de base de datos."""
        self.db = db

    def crear_premio(
        self,
        juego_id: UUID,
        descripcion: str,
        valor: float,
        creado_por: Optional[str] = None,
    ) -> Premio:
        """
        Crea un nuevo premio y lo guarda en la base de datos
        """
        premio = Premio(
            juego_id=juego_id,
            descripcion=descripcion,
            valor=valor,
            creado_por=creado_por,
        )
        self.db.add(premio)
        self.db.commit()
        self.db.refresh(premio)
        return premio

    def obtener_premio(self, premio_id: UUID) -> Optional[Premio]:
        """
        Obtiene un premio por su ID.
        """
        return self.db.query(Premio).filter(Premio.id == premio_id).first()

    def obtener_premios(self, skip: int = 0, limit: int = 100) -> List[Premio]:
        """
        Obtiene todos los premios con paginación opcional.
        """
        return self.db.query(Premio).offset(skip).limit(limit).all()

    def actualizar_premio(
        self,
        premio_id: UUID,
        descripcion: Optional[str] = None,
        valor: Optional[float] = None,
        juego_id: Optional[UUID] = None,
        actualizado_por: Optional[str] = None,
    ) -> Optional[Premio]:
        """
        Actualiza los atributos de un premio existente.
        """
        premio = self.db.query(Premio).filter(Premio.id == premio_id).first()
        if not premio:
            return None

        if descripcion is not None:
            premio.descripcion = descripcion
        if valor is not None:
            premio.valor = valor
        if juego_id is not None:
            premio.juego_id = juego_id

        if actualizado_por is not None:
            premio.actualizado_por = actualizado_por

        try:
            self.db.commit()
            self.db.refresh(premio)
            return premio
        except IntegrityError:
            self.db.rollback()
            return None

    def eliminar_premio(self, premio_id: UUID) -> bool:
        """
        Elimina un premio por su ID.
        """
        premio = self.db.query(Premio).filter(Premio.id == premio_id).first()
        if not premio:
            return False

        try:
            self.db.delete(premio)
            self.db.commit()
            return True
        except IntegrityError:

            self.db.rollback()
            return False
        except Exception as e:
            self.db.rollback()
            print(f"Error desconocido al eliminar premio: {e}")
            return False
