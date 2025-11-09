"""
API de Historial de Saldo - Endpoints para gestión del historial de movimientos
"""

from typing import List, Optional
from uuid import UUID
from crud.historial_saldo_crud import HistorialSaldoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas import (
    HistorialSaldoCreate,
    HistorialSaldoResponse,
    HistorialSaldoUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import (
    IntegrityError,
)  # Importación clave para manejar errores de FK

router = APIRouter(prefix="/historial-saldo", tags=["historial_saldo"])


@router.get("/", response_model=List[HistorialSaldoResponse])
async def obtener_historial(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Obtener el historial de movimientos de saldo."""
    try:
        #  Instanciar la clase CRUD
        crud = HistorialSaldoCRUD(db)
        #  Llamar al método de la instancia
        return crud.obtener_todos(
            skip=skip, limit=limit
        )  # Asumo que tu método es 'obtener_todos'
    except Exception as e:
        # Si tienes paginación avanzada, el error puede estar en la serialización.
        raise HTTPException(
            status_code=500, detail=f"Error al obtener historial: {str(e)}"
        )


@router.get("/{historial_id}", response_model=HistorialSaldoResponse)
async def obtener_historial_por_id(historial_id: UUID, db: Session = Depends(get_db)):
    """Obtener un registro de historial de saldo por su ID."""
    try:
        # Instanciar la clase CRUD
        crud = HistorialSaldoCRUD(db)
        registro = crud.obtener_por_id(historial_id)
        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return registro
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener registro: {str(e)}"
        )


@router.post(
    "/", response_model=HistorialSaldoResponse, status_code=status.HTTP_201_CREATED
)
async def crear_historial(
    historial_data: HistorialSaldoCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo registro en el historial de saldo."""
    #  Instanciar la clase CRUD
    crud = HistorialSaldoCRUD(db)

    try:
        # Llamar al método de la instancia
        return crud.crear_movimiento(
            usuario_id=historial_data.usuario_id,
            tipo=historial_data.tipo,
            monto=historial_data.monto,
        )
    except IntegrityError:
        # Capturar error de FK y devolver 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Violación de Clave Foránea: Asegúrese que el 'usuario_id' es un UUID de un usuario existente.",
        )
    except Exception as e:
        # Para otros errores internos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear registro: {str(e)}",
        )


@router.put("/{historial_id}", response_model=HistorialSaldoResponse)
async def actualizar_historial(
    historial_id: UUID,
    historial_data: HistorialSaldoUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un registro existente del historial de saldo."""
    try:
        #  Instanciar la clase CRUD
        crud = HistorialSaldoCRUD(db)
        registro = crud.obtener_por_id(historial_id)
        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        campos = historial_data.model_dump(
            exclude_unset=True
        )  # Uso moderno de Pydantic V2
        # Asumo que tienes un método 'actualizar_registro' en tu CRUD
        return crud.actualizar_registro(historial_id, **campos)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar registro: {str(e)}"
        )


@router.delete("/{historial_id}", response_model=RespuestaAPI)
async def eliminar_historial(historial_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un registro del historial de saldo."""
    try:
        #  Instanciar la clase CRUD
        crud = HistorialSaldoCRUD(db)
        registro = crud.obtener_por_id(historial_id)
        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        eliminado = crud.eliminar_movimiento(historial_id)
        if eliminado:
            return RespuestaAPI(mensaje="Registro eliminado exitosamente", exito=True)

        raise HTTPException(status_code=500, detail="Error al eliminar registro")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar registro: {str(e)}"
        )
