from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.juego_crud import JuegoCRUD
from schemas import JuegoCreate, JuegoUpdate, JuegoResponse
from uuid import UUID
from typing import List

router = APIRouter(prefix="/juegos", tags=["Juegos"])


@router.get("/", response_model=List[JuegoResponse])
def obtener_juegos(db: Session = Depends(get_db)):
    """
    Obtiene todos los juegos.
    """
    return JuegoCRUD(db).obtener_juegos()


@router.get("/{juego_id}", response_model=JuegoResponse)
def obtener_juego(juego_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene un juego por ID.
    """
    juego = JuegoCRUD(db).obtener_juego(juego_id)
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego


@router.post("/", response_model=JuegoResponse)
def crear_juego(data: JuegoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo juego.
    """
    return JuegoCRUD(db).crear_juego(
        data.nombre,
        data.descripcion,
        data.costo_base,
        data.creado_por,
    )


@router.put("/{juego_id}", response_model=JuegoResponse)
def actualizar_juego(juego_id: UUID, data: JuegoUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un juego.
    """
    juego = JuegoCRUD(db).actualizar_juego(
        juego_id,
        data.nombre,
        data.descripcion,
        data.costo_base,
        data.actualizado_por,
    )
    if not juego:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return juego


@router.delete("/{juego_id}")
def eliminar_juego(juego_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un juego.
    """
    exito = JuegoCRUD(db).eliminar_juego(juego_id)
    if not exito:
        raise HTTPException(
            status_code=409, detail="No se puede eliminar. Existen registros asociados."
        )
    return {"mensaje": "Juego eliminado correctamente", "exito": True}
