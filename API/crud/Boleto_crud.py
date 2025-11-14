"""
Operaciones CRUD para Boleto
============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Boleto.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from entities.Boleto import Boleto
from uuid import UUID


class BoletoCRUD:
    """Clase para operaciones CRUD de Boleto"""

    def __init__(self, db: Session):
        self.db = db

    def crear_boleto(
        self,
        usuario_id: UUID,
        juego_id: UUID,
        numeros: Optional[str],
        costo: float,
        creado_por: Optional[str] = None,
    ) -> Boleto:
        """
        Crea un nuevo boleto en la base de datos.
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

    def obtener_por_id(self, boleto_id: UUID) -> Optional[Boleto]:
        """
        Obtiene un boleto por su ID.
        """
        return self.db.query(Boleto).filter(Boleto.id == boleto_id).first()

    def obtener_todos(self, skip: int = 0, limit: int = 100) -> List[Boleto]:
        return self.db.query(Boleto).offset(skip).limit(limit).all()

    def actualizar_boleto(
        self,
        boleto_id: UUID,
        numeros: Optional[str] = None,
        costo: Optional[float] = None,
        actualizado_por: Optional[str] = None,
    ) -> Optional[Boleto]:
        """
        Actualiza los datos de un boleto existente.
        """
        boleto = self.db.query(Boleto).filter(Boleto.id == boleto_id).first()
        if not boleto:
            return None

        if numeros is not None:
            boleto.numeros = numeros

        if costo is not None:
            boleto.costo = costo

        if actualizado_por is not None:
            boleto.actualizado_por = actualizado_por

        self.db.commit()
        self.db.refresh(boleto)
        return boleto

    def eliminar_boleto(self, boleto_id: UUID) -> bool:
        """
        Elimina un boleto de la base de datos.
        """
        boleto = self.db.query(Boleto).filter(Boleto.id == boleto_id).first()
        if not boleto:
            return False
        self.db.delete(boleto)
        self.db.commit()
        return True
