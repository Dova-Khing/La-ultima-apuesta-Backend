"""
Operaciones CRUD para Boleto
============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Boleto.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from ORM.entities.Boleto import Boleto


class BoletoCRUD:
    """Clase para operaciones CRUD de Boleto"""

    def __init__(self, db: Session):
        self.db = db

    def crear_boleto(
        self,
        usuario_id: int,
        juego_id: int,
        numeros: Optional[str],
        costo: float,
        creado_por: Optional[str] = None,
    ) -> Boleto:
        """
        Crea un nuevo boleto en la base de datos.

        Args:
            usuario_id (int): ID del usuario que compra el boleto.
            juego_id (int): ID del juego asociado al boleto.
            numeros (Optional[str]): Números seleccionados en el boleto.
            costo (float): Costo del boleto.
            creado_por (Optional[str], optional): Usuario que creó el registro.

        Returns:
            Boleto: Objeto Boleto recién creado.

        """
        boleto = Boleto(
            usuario_id=usuario_id,
            juego_id=juego_id,
            numeros=numeros,
            costo=costo,
            creado_por=creado_por,
        )
        self.db.add(boleto)
        self.db.commit()
        self.db.refresh(boleto)
        return boleto

    def obtener_por_id(self, boleto_id: int) -> Optional[Boleto]:
        """
          Obtiene un boleto por su ID.

        Args:
            boleto_id (int): ID del boleto.

        Returns:
            Optional[Boleto]: Objeto Boleto si existe, None si no se encuentra.


        """
        return self.db.query(Boleto).filter(Boleto.id == boleto_id).first()

    def obtener_todos(self, skip: int = 0, limit: int = 100) -> List[Boleto]:
        return self.db.query(Boleto).offset(skip).limit(limit).all()

    def actualizar_boleto(
        self,
        boleto_id: int,
        numeros: Optional[str] = None,
        actualizado_por: Optional[str] = None,
    ) -> Optional[Boleto]:
        """
          Actualiza los datos de un boleto existente.

        Args:
            boleto_id (int): ID del boleto a actualizar.
            numeros (Optional[str], optional): Números nuevos del boleto.
            actualizado_por (Optional[str], optional): Usuario que realiza la actualización.

        Returns:
            Optional[Boleto]: Objeto Boleto actualizado si existe, None si no se encuentra.


        """
        boleto = self.db.query(Boleto).filter(Boleto.id == boleto_id).first()
        if not boleto:
            return None

        if numeros is not None:
            boleto.numeros = numeros
        if actualizado_por is not None:
            boleto.actualizado_por = actualizado_por

        self.db.commit()
        self.db.refresh(boleto)
        return boleto

    def eliminar_boleto(self, boleto_id: int) -> bool:
        """
        Elimina un boleto de la base de datos.

        Args:
            boleto_id (int): ID del boleto a eliminar.

        Returns:
            bool: True si el boleto fue eliminado, False si no se encontró.


        """
        boleto = self.db.query(Boleto).filter(Boleto.id == boleto_id).first()
        if not boleto:
            return False
        self.db.delete(boleto)
        self.db.commit()
        return True
