"""
API de Premios - Endpoints para gestión de premios
"""

from typing import List
from uuid import UUID

from crud.premio_crud import PremioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PremioCreate, PremioResponse, PremioUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/premios", tags=["premios"])


@router.get("/", response_model=List[PremioResponse])
async def obtener_premios(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
     Obtener todos los premios con paginación.

    Args:
        skip (int): Número de registros a omitir (para paginación). Default 0.
        limit (int): Número máximo de registros a devolver. Default 100.
        db (Session): Sesión de base de datos proporcionada por `Depends(get_db)`.

    Returns:
        List[PremioResponse]: Lista de premios almacenados en la base de datos.

    Raises:
        HTTPException(500): Si ocurre un error interno al obtener los premios.
    """

    try:
        premio_crud = PremioCRUD(db)
        premios = premio_crud.obtener_premios(skip=skip, limit=limit)
        return premios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener premios: {str(e)}",
        )


@router.get("/{premio_id}", response_model=PremioResponse)
async def obtener_premio(premio_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un premio por su ID.

    Args:
        premio_id (UUID): Identificador único del premio.
        db (Session): Sesión de base de datos.

    Returns:
        PremioResponse: Datos del premio encontrado.

    Raises:
        HTTPException(404): Si no se encuentra el premio.
        HTTPException(500): Si ocurre un error inesperado al consultar.

    """
    try:
        premio_crud = PremioCRUD(db)
        premio = premio_crud.obtener_premio(premio_id)
        if not premio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Premio no encontrado"
            )
        return premio
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener premio: {str(e)}",
        )


@router.post("/", response_model=PremioResponse, status_code=status.HTTP_201_CREATED)
async def crear_premio(premio_data: PremioCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo premio.

    Args:
        premio_data (PremioCreate): Datos requeridos para crear el premio.
        db (Session): Sesión de base de datos.

    Returns:
        PremioResponse: Datos del premio creado.

    Raises:
        HTTPException(400): Si los datos de entrada no son válidos.
        HTTPException(500): Si ocurre un error interno al crear el premio.

    """
    try:
        premio_crud = PremioCRUD(db)
        premio = premio_crud.crear_premio(
            juego_id=premio_data.juego_id,
            descripcion=premio_data.descripcion,
            valor=premio_data.valor,
            creado_por=premio_data.creado_por,
        )
        return premio
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear premio: {str(e)}",
        )


@router.put("/{premio_id}", response_model=PremioResponse)
async def actualizar_premio(
    premio_id: UUID, premio_data: PremioUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar un premio existente.

    Args:
        premio_id (UUID): Identificador único del premio a actualizar.
        premio_data (PremioUpdate): Campos a modificar (solo los no nulos se actualizan).
        db (Session): Sesión de base de datos.

    Returns:
        PremioResponse: Datos del premio actualizado.

    Raises:
        HTTPException(404): Si el premio no existe.
        HTTPException(400): Si los datos proporcionados son inválidos.
        HTTPException(500): Si ocurre un error interno al actualizar el premio.

    """
    try:
        premio_crud = PremioCRUD(db)
        premio_existente = premio_crud.obtener_premio(premio_id)
        if not premio_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Premio no encontrado"
            )

        campos_actualizacion = {
            k: v for k, v in premio_data.dict().items() if v is not None
        }
        if not campos_actualizacion:
            return premio_existente

        premio_actualizado = premio_crud.actualizar_premio(
            premio_id, **campos_actualizacion
        )
        return premio_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar premio: {str(e)}",
        )


@router.delete("/{premio_id}", response_model=RespuestaAPI)
async def eliminar_premio(premio_id: UUID, db: Session = Depends(get_db)):
    """
    Eliminar un premio por su ID.

    Args:
        premio_id (UUID): Identificador único del premio a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de confirmación y estado de éxito.

    Raises:
        HTTPException(404): Si el premio no existe.
        HTTPException(500): Si ocurre un error interno al eliminar el premio.

    """
    try:
        premio_crud = PremioCRUD(db)
        premio_existente = premio_crud.obtener_premio(premio_id)
        if not premio_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Premio no encontrado"
            )

        eliminada = premio_crud.eliminar_premio(premio_id)
        if eliminada:
            return RespuestaAPI(mensaje="Premio eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar premio",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar premio: {str(e)}",
        )
