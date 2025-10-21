"""
Operaciones CRUD para Usuario
"""

import re
from typing import List, Optional
from uuid import UUID

from ORM.auth.security import PasswordManager
from ORM.entities.usuario import Usuario
from sqlalchemy.orm import Session


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    def _validar_email(self, email: str) -> bool:
        """Validar formato de email"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """Validar formato de teléfono"""
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def _validar_nombre_usuario(self, nombre_usuario: str) -> bool:
        """Validar formato de nombre de usuario"""
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return re.match(pattern, nombre_usuario) is not None

    def crear_usuario(
        self,
        nombre: str,
        nombre_usuario: str,
        email: str,
        contrasena: str,
        telefono: Optional[str] = None,
        edad: Optional[int] = None,
        saldo_inicial: Optional[int] = None,
        es_admin: bool = False,
    ) -> Usuario:
        """
        Crear un nuevo usuario con validaciones
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")

        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if not nombre_usuario or not self._validar_nombre_usuario(nombre_usuario):
            raise ValueError(
                "El nombre de usuario debe tener entre 3-20 caracteres y solo contener letras, números y guiones bajos"
            )

        if self.obtener_usuario_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya está registrado")

        if not email or not self._validar_email(email):
            raise ValueError("Email inválido")

        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado")

        if not contrasena:
            raise ValueError("La contraseña es obligatoria")

        es_valida, mensaje = PasswordManager.validate_password_strength(contrasena)
        if not es_valida:
            raise ValueError(f"Contraseña inválida: {mensaje}")

        if telefono and not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        contrasena_hash = PasswordManager.hash_password(contrasena)

        usuario = Usuario(
            nombre=nombre.strip(),
            nombre_usuario=nombre_usuario.strip().lower(),
            email=email.strip().lower(),
            telefono=telefono,
            contrasena_hash=contrasena_hash,
            edad=edad,
            saldo_inicial=saldo_inicial,
            es_admin=es_admin,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """Obtener un usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Obtener un usuario por email"""
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email.lower().strip())
            .first()
        )

    def obtener_usuario_por_nombre_usuario(
        self, nombre_usuario: str
    ) -> Optional[Usuario]:
        """Obtener un usuario por nombre de usuario"""
        return (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario.lower().strip())
            .first()
        )

    def autenticar_usuario(
        self, nombre_usuario: str, contrasena: str
    ) -> Optional[Usuario]:
        """Autenticar un usuario con nombre de usuario o email y contraseña"""
        usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            usuario = self.obtener_usuario_por_email(nombre_usuario)

        if not usuario or not usuario.activo:
            return None

        if PasswordManager.verify_password(contrasena, usuario.contrasena_hash):
            return usuario

        return None

    def cambiar_contrasena(
        self, usuario_id: UUID, contrasena_actual: str, nueva_contrasena: str
    ) -> bool:
        """Cambiar la contraseña de un usuario"""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False

        if not PasswordManager.verify_password(
            contrasena_actual, usuario.contrasena_hash
        ):
            raise ValueError("La contraseña actual es incorrecta")

        es_valida, mensaje = PasswordManager.validate_password_strength(
            nueva_contrasena
        )
        if not es_valida:
            raise ValueError(f"Nueva contraseña inválida: {mensaje}")

        usuario.contrasena_hash = PasswordManager.hash_password(nueva_contrasena)
        self.db.commit()
        return True

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtener lista de usuarios con paginación"""
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        """Actualizar un usuario con validaciones"""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "email" in kwargs:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_usuario_por_email(email)
                and self.obtener_usuario_por_email(email).id != usuario_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            if not self._validar_telefono(kwargs["telefono"]):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "nombre_usuario" in kwargs:
            nombre_usuario = kwargs["nombre_usuario"]
            if not nombre_usuario or not self._validar_nombre_usuario(nombre_usuario):
                raise ValueError(
                    "El nombre de usuario debe tener entre 3-20 caracteres y solo contener letras, números y guiones bajos"
                )
            if (
                self.obtener_usuario_por_nombre_usuario(nombre_usuario)
                and self.obtener_usuario_por_nombre_usuario(nombre_usuario).id
                != usuario_id
            ):
                raise ValueError("El nombre de usuario ya está registrado")
            kwargs["nombre_usuario"] = nombre_usuario.strip().lower()

        if "contrasena" in kwargs:
            contrasena = kwargs["contrasena"]
            es_valida, mensaje = PasswordManager.validate_password_strength(contrasena)
            if not es_valida:
                raise ValueError(f"Contraseña inválida: {mensaje}")
            kwargs["contrasena_hash"] = PasswordManager.hash_password(contrasena)
            del kwargs["contrasena"]

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        """Eliminar un usuario"""
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """Desactivar un usuario (soft delete)"""
        return self.actualizar_usuario(usuario_id, activo=False)

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """Obtener todos los usuarios administradores"""
        return self.db.query(Usuario).filter(Usuario.es_admin == True).all()

    def es_admin(self, usuario_id: UUID) -> bool:
        """Verificar si un usuario es administrador"""
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        """Obtener el usuario administrador por defecto"""
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == "admin@system.com", Usuario.es_admin == True)
            .first()
        )
