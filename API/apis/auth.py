from uuid import UUID

from ORM.crud.usuario_crud import UsuarioCRUD
from ORM.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from ORM.schemas import RespuestaAPI, UsuarioLogin, UsuarioResponse
from sqlalchemy.orm import Session
import re

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/login", response_model=UsuarioResponse)
async def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    """
     Autenticar un usuario con nombre de usuario/email y contraseña.

    Parámetros (body):
        login_data (UsuarioLogin): Contiene las credenciales de inicio de sesión.
            - nombre_usuario (str): Nombre de usuario o email del usuario.
            - contraseña (str): Contraseña asociada.

        db (Session): Sesión de base de datos.

    Retorna:
        UsuarioResponse: Información del usuario autenticado si las credenciales son válidas.

    Errores:
        401 UNAUTHORIZED: Credenciales incorrectas o usuario inactivo.
        500 INTERNAL_SERVER_ERROR: Error en el proceso de autenticación.
    """
    try:
        if not login_data.nombre_usuario or not login_data.contraseña:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario/email y la contraseña son obligatorios",
            )

        if len(login_data.contraseña) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 8 caracteres",
            )

        if "@" in login_data.nombre_usuario:
            patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(patron_email, login_data.nombre_usuario):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El formato del email no es válido",
                )

        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.autenticar_usuario(
            login_data.nombre_usuario, login_data.contraseña
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas o usuario inactivo",
            )

        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error durante el login:{str(e)}",
        )


@router.post("/crear-admin", response_model=RespuestaAPI)
async def crear_usuario_admin(db: Session = Depends(get_db)):
    """
     Crear un usuario administrador por defecto.

    Parámetros:
        db (Session): Sesión de base de datos.

    Retorna:
        RespuestaAPI: Mensaje de confirmación y credenciales temporales del administrador creado.

    Notas:
        - Si ya existe un administrador por defecto, retorna la información del existente.
        - Genera una contraseña segura temporal que debe cambiarse en el primer inicio de sesión.

    Errores:
        400 BAD_REQUEST: Error en los datos enviados.
        500 INTERNAL_SERVER_ERROR: Fallo al crear el administrador.
    """
    try:
        usuario_crud = UsuarioCRUD(db)

        admin_existente = usuario_crud.obtener_admin_por_defecto()
        if admin_existente:
            return RespuestaAPI(
                mensaje="Ya existe un usuario administrador por defecto",
                exito=True,
                datos={"admin_id": str(admin_existente.id)},
            )

        from auth.security import PasswordManager

        contrasena_admin = PasswordManager.generate_secure_password(12)

        admin = usuario_crud.crear_usuario(
            nombre="Administrador del Sistema",
            nombre_usuario="admin",
            email="admin@system.com",
            contrasena=contrasena_admin,
            edad="99",
            saldo_inicial=0,
            es_admin=True,
        )

        return RespuestaAPI(
            mensaje="Usuario administrador creado exitosamente",
            exito=True,
            datos={
                "admin_id": str(admin.id),
                "contrasena_temporal": contrasena_admin,
                "mensaje": "IMPORTANTE: Cambie esta contraseña en su primer inicio de sesión",
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear administrador: {str(e)}",
        )


@router.get("/verificar/{usuario_id}", response_model=RespuestaAPI)
async def verificar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """
    Verificar si un usuario existe y se encuentra activo en el sistema.

    Parámetros (path):
        usuario_id (UUID): Identificador único del usuario.

        db (Session): Sesión de base de datos.

    Retorna:
        RespuestaAPI: Información del usuario, incluyendo:
            - usuario_id (UUID)
            - nombre (str)
            - email (str)
            - edad (int)
            - saldo_inicial (float)
            - activo (bool)
            - es_admin (bool)

    Errores:
        404 NOT_FOUND: Si el usuario no existe.
        500 INTERNAL_SERVER_ERROR: Error en la verificación.
    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario(usuario_id)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return RespuestaAPI(
            mensaje="Usuario verificado exitosamente",
            exito=True,
            datos={
                "usuario_id": str(usuario.id),
                "nombre": usuario.nombre,
                "email": usuario.email,
                "edad": usuario.edad,
                "saldo_inicial": usuario.saldo_inicial,
                "activo": usuario.activo,
                "es_admin": usuario.es_admin,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar usuario: {str(e)}",
        )


@router.get("/estado", response_model=RespuestaAPI)
async def estado_autenticacion():
    """
     Verificar el estado del sistema de autenticación.

    Parámetros:
        Ninguno.

    Retorna:
        RespuestaAPI: Estado actual del sistema de autenticación, incluyendo:
            - sistema (str): Nombre del sistema.
            - version (str): Versión actual del sistema.
            - autenticacion (str): Estado del módulo de autenticación.

    Uso:
        Permite verificar rápidamente si el servicio de autenticación está en funcionamiento.
    """
    return RespuestaAPI(
        mensaje="Sistema de autenticación funcionando correctamente",
        exito=True,
        datos={
            "sistema": "Sistema de Gestión de Juegos y Apuestas",
            "version": "1.0.0",
            "autenticacion": "Activa",
        },
    )
