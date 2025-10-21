"""
API de Partidas - Endpoints para gestión de partidas
"""

from typing import List
from uuid import UUID

from ORM.crud.partida_crud import PartidaCRUD
from ORM.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from ORM.schemas import PartidaCreate, PartidaResponse, PartidaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/partidas", tags=["partidas"])


@router.get("/", response_model=List[PartidaResponse])
async def obtener_partidas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener una lista de partidas.

    Args:
        skip (int, opcional): Número de registros a omitir. Por defecto 0.
        limit (int, opcional): Número máximo de partidas a devolver. Por defecto 100.
        db (Session): Sesión de base de datos proporcionada por dependencia.

    Returns:
        List[PartidaResponse]: Lista de partidas registradas en el sistema.

    Raises:
        HTTPException(500): Si ocurre un error inesperado al obtener las partidas.


    """
    try:
        return PartidaCRUD.obtener_todas(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener partidas: {str(e)}"
        )


@router.get("/{partida_id}", response_model=PartidaResponse)
async def obtener_partida(partida_id: UUID, db: Session = Depends(get_db)):
    """
     Obtener una partida específica por su ID.

    Args:
        partida_id (UUID): Identificador único de la partida.
        db (Session): Sesión de base de datos proporcionada por dependencia.

    Returns:
        PartidaResponse: Información de la partida solicitada.

    Raises:
        HTTPException(404): Si la partida no se encuentra.
        HTTPException(500): Si ocurre un error inesperado al consultar.


    """
    try:
        partida = PartidaCRUD.obtener_por_id(db, partida_id)
        if not partida:
            raise HTTPException(status_code=404, detail="Partida no encontrada")
        return partida
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener partida: {str(e)}"
        )


@router.post("/", response_model=PartidaResponse, status_code=201)
async def crear_partida(partida_data: PartidaCreate, db: Session = Depends(get_db)):
    """
     Crear una nueva partida en el sistema.

    Args:
        partida_data (PartidaCreate): Datos necesarios para la creación de la partida.
        db (Session): Sesión de base de datos proporcionada por dependencia.

    Returns:
        PartidaResponse: Información de la partida recién creada.

    Raises:
        HTTPException(500): Si ocurre un error inesperado al crear la partida.


    """
    try:
        return PartidaCRUD.crear_partida(db, **partida_data.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear partida: {str(e)}")


@router.put("/{partida_id}", response_model=PartidaResponse)
async def actualizar_partida(
    partida_id: UUID, partida_data: PartidaUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar los datos de una partida existente.

    Args:
        partida_id (UUID): Identificador único de la partida a actualizar.
        partida_data (PartidaUpdate): Datos a modificar en la partida.
        db (Session): Sesión de base de datos proporcionada por dependencia.

    Returns:
        PartidaResponse: Información de la partida actualizada.

    Raises:
        HTTPException(404): Si la partida no existe.
        HTTPException(500): Si ocurre un error inesperado al actualizar.


    """
    try:
        partida = PartidaCRUD.obtener_por_id(db, partida_id)
        if not partida:
            raise HTTPException(status_code=404, detail="Partida no encontrada")

        campos = {k: v for k, v in partida_data.dict().items() if v is not None}
        return PartidaCRUD.actualizar_partida(db, partida_id, **campos)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar partida: {str(e)}"
        )


@router.delete("/{partida_id}", response_model=RespuestaAPI)
async def eliminar_partida(partida_id: UUID, db: Session = Depends(get_db)):
    """
       Eliminar una partida por su ID.

    Args:
        partida_id (UUID): Identificador único de la partida a eliminar.
        db (Session): Sesión de base de datos proporcionada por dependencia.

    Returns:
        RespuestaAPI: Mensaje de confirmación y estado de la operación.

    Raises:
        HTTPException(404): Si la partida no se encuentra.
        HTTPException(500): Si ocurre un error inesperado al eliminar.


    """
    try:
        partida = PartidaCRUD.obtener_por_id(db, partida_id)
        if not partida:
            raise HTTPException(status_code=404, detail="Partida no encontrada")

        eliminado = PartidaCRUD.eliminar_partida(db, partida_id)
        if eliminado:
            return RespuestaAPI(mensaje="Partida eliminada exitosamente", exito=True)
        raise HTTPException(status_code=500, detail="Error al eliminar partida")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar partida: {str(e)}"
        )
