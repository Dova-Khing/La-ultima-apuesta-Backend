from uuid import UUID

from crud.usuario_crud import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import RespuestaAPI, UsuarioLogin, UsuarioResponse
from sqlalchemy.orm import Session
import re

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/login", response_model=UsuarioResponse)
async def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        print(f"Intento de login recibido:")
        print(f"Nombre usuario: {login_data.nombre_usuario}")
        print(f"Contraseña length: {len(login_data.contrasena)}")

        if not login_data.nombre_usuario or not login_data.contrasena:
            print("Campos vacíos")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario/email y la contraseña son obligatorios",
            )

        if len(login_data.contrasena) < 8:
            print("Contraseña muy corta")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 8 caracteres",
            )

        usuario_crud = UsuarioCRUD(db)
        print("Llamando a autenticar_usuario...")

        usuario = usuario_crud.autenticar_usuario(
            login_data.nombre_usuario, login_data.contrasena
        )

        if not usuario:
            print(
                "autenticar_usuario retornó None - credenciales incorrectas o usuario inactivo"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas o usuario inactivo",
            )

        print(f"Login exitoso para: {usuario.nombre}")
        return usuario

    except HTTPException:
        print("HTTPException en login")
        raise
    except Exception as e:
        print(f"ERROR inesperado en login: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error durante el login:{str(e)}",
        )
