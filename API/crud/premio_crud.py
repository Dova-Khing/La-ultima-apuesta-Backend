"""
Operaciones CRUD para Premio
============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Premio.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from ORM.entities.premio import Premio


class PremioCRUD:
    """Clase para operaciones CRUD de Premio"""

    def __init__(self, db: Session):
        """Inicializa la clase con la sesión de base de datos."""
        self.db = db

    def crear_premio(
        db: Session,
        juego_id: int,
        descripcion: str,
        valor: float,
        creado_por: Optional[str] = None,
    ) -> Premio:
        """
        Crea un nuevo premio y lo guarda en la base de datos

        Args:
        db (Session): Sesión de base de datos.
            juego_id (int): ID del juego asociado.
            descripcion (str): Descripción del premio.
            valor (float): Valor del premio.
            creado_por (Optional[str]): Nombre del usuario que creó el premio.

        Returns:
            Premio: Instancia del premio creado.

        """

        premio = Premio(
            juego_id=juego_id,
            descripcion=descripcion,
            valor=valor,
            creado_por=creado_por,
        )
        db.add(premio)
        db.commit()
        db.refresh(premio)
        return premio

    def obtener_por_id(db: Session, premio_id: int) -> Optional[Premio]:
        """
         Obtiene un premio por su ID.

        Args:
            db (Session): Sesión de base de datos.
            premio_id (int): ID del premio.

        Returns:
            Optional[Premio]: Instancia del premio o None si no existe.

        """
        return db.query(Premio).filter(Premio.id == premio_id).first()

    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Premio]:
        """
        Obtiene todos los premios con paginación opcional.

        Args:
            db (Session): Sesión de base de datos.
            skip (int): Número de registros a saltar.
            limit (int): Número máximo de registros a retornar.

        Returns:
            List[Premio]: Lista de premios.

        """

        return db.query(Premio).offset(skip).limit(limit).all()

    def actualizar_premio(
        db: Session,
        premio_id: int,
        descripcion: Optional[str] = None,
        valor: Optional[float] = None,
        actualizado_por: Optional[str] = None,
    ) -> Optional[Premio]:
        """
        Actualiza los atributos de un premio existente.

        Args:
            db (Session): Sesión de base de datos.
            premio_id (int): ID del premio a actualizar.
            descripcion (Optional[str]): Nueva descripción.
            valor (Optional[float]): Nuevo valor.
            actualizado_por (Optional[str]): Usuario que realiza la actualización.

        Returns:
            Optional[Premio]: Premio actualizado o None si no existe

        """
        premio = db.query(Premio).filter(Premio.id == premio_id).first()
        if not premio:
            return None

        if descripcion is not None:
            premio.descripcion = descripcion
        if valor is not None:
            premio.valor = valor
        if actualizado_por is not None:
            premio.actualizado_por = actualizado_por

        db.commit()
        db.refresh(premio)
        return premio

    def eliminar_premio(db: Session, premio_id: int) -> bool:
        """
        Elimina un premio por su ID.

        Args:
            db (Session): Sesión de base de datos.
            premio_id (int): ID del premio a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existe.

        """
        premio = db.query(Premio).filter(Premio.id == premio_id).first()
        if not premio:
            return False
        db.delete(premio)
        db.commit()
        return True
