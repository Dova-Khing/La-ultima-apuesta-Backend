"""
Operaciones CRUD para Juego
===========================

Este módulo contiene todas las operaciones de base de datos
para la entidad Juego.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from ORM.entities.juego import Juego


class JuegoCRUD:
    """Clase para operaciones CRUD de Juego"""

    def __init__(self, db: Session):
        self.db = db

    def crear_juego(
        db: Session,
        nombre: str,
        descripcion: Optional[str],
        costo_base: float,
        creado_por: Optional[str] = None,
    ) -> Juego:
        """
         Crea un nuevo juego en la base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            nombre (str): Nombre del juego.
            descripcion (Optional[str]): Descripción del juego.
            costo_base (float): Costo base del juego.
            creado_por (Optional[str]): Usuario que crea el juego.

        Returns:
            Juego: Objeto Juego creado y persistido en la base de datos.

        """
        juego = Juego(
            nombre=nombre,
            descripcion=descripcion,
            costo_base=costo_base,
            creado_por=creado_por,
        )
        db.add(juego)
        db.commit()
        db.refresh(juego)
        return juego

    def obtener_por_id(db: Session, juego_id: int) -> Optional[Juego]:
        """
         Obtiene un juego por su ID.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            juego_id (int): ID del juego a buscar.

        Returns:
            Optional[Juego]: Objeto Juego si existe, None si no.
        """
        return db.query(Juego).filter(Juego.id == juego_id).first()

    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Juego]:
        """

         Obtiene todos los juegos, con soporte para paginación.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            skip (int, optional): Número de registros a omitir. Por defecto 0.
            limit (int, optional): Número máximo de registros a devolver. Por defecto 100.

        Returns:
            List[Juego]: Lista de juegos obtenidos.

        """
        return db.query(Juego).offset(skip).limit(limit).all()

    def actualizar_juego(
        db: Session,
        juego_id: int,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        costo_base: Optional[float] = None,
        actualizado_por: Optional[str] = None,
    ) -> Optional[Juego]:
        """
        Actualiza un juego existente por su ID.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            juego_id (int): ID del juego a actualizar.
            nombre (Optional[str]): Nuevo nombre del juego.
            descripcion (Optional[str]): Nueva descripción.
            costo_base (Optional[float]): Nuevo costo base.
            actualizado_por (Optional[str]): Usuario que realiza la actualización.

        Returns:
            Optional[Juego]: Objeto Juego actualizado, o None si no se encontró.

        """
        juego = db.query(Juego).filter(Juego.id == juego_id).first()
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

        db.commit()
        db.refresh(juego)
        return juego

    def eliminar_juego(db: Session, juego_id: int) -> bool:
        """

         Elimina un juego por su ID.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
            juego_id (int): ID del juego a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existe.
        """
        juego = db.query(Juego).filter(Juego.id == juego_id).first()
        if not juego:
            return False
        db.delete(juego)
        db.commit()
        return True
