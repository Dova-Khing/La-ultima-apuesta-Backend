"""
Módulo de seguridad para manejo de contraseñas y tokens JWT
"""

import hashlib
import secrets
from typing import Tuple
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os


SECRET_KEY = os.getenv(
    "SECRET_KEY", "tu_clave_secreta_muy_segura_aqui_cambiar_en_produccion"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


class PasswordManager:
    """Gestor de contraseñas con hash seguro"""

    # ... (tu código actual se mantiene igual)
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Generar hash seguro de una contraseña

        Args:
            password: Contraseña en texto plano

        Returns:
            Hash de la contraseña con salt
        """
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return f"{salt}:{password_hash.hex()}"

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verificar si una contraseña coincide con su hash

        Args:
            password: Contraseña en texto plano
            password_hash: Hash almacenado

        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            salt, hash_part = password_hash.split(":")
            password_hash_check = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
            )
            return password_hash_check.hex() == hash_part
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """
        Validar la fortaleza de una contraseña

        Args:
            password: Contraseña a validar

        Returns:
            Tupla con (es_válida, mensaje)
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"

        if len(password) > 128:
            return False, "La contraseña no puede exceder 128 caracteres"

        if not any(c.isupper() for c in password):
            return False, "La contraseña debe contener al menos una letra mayúscula"

        if not any(c.islower() for c in password):
            return False, "La contraseña debe contener al menos una letra minúscula"

        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe contener al menos un número"

        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "La contraseña debe contener al menos un carácter especial"

        return True, "Contraseña válida"

    @staticmethod
    def generate_secure_password(length: int = 12) -> str:
        """
        Generar una contraseña segura aleatoria

        Args:
            length: Longitud de la contraseña

        Returns:
            Contraseña segura generada
        """
        import string

        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = "".join(secrets.choice(characters) for _ in range(length))
        return password


class TokenManager:
    """Gestor de tokens JWT"""

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """
        Crear un token JWT de acceso

        Args:
            data: Datos a incluir en el token
            expires_delta: Tiempo de expiración personalizado

        Returns:
            Token JWT codificado
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update(
            {
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "access_token",
            }
        )

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verificar y decodificar un token JWT

        Args:
            token: Token JWT a verificar

        Returns:
            Payload del token si es válido

        Raises:
            JWTError: Si el token es inválido o ha expirado
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            raise JWTError(f"Token inválido: {str(e)}")

    @staticmethod
    def get_user_id_from_token(token: str) -> str:
        """
        Obtener el ID de usuario desde un token JWT

        Args:
            token: Token JWT

        Returns:
            ID del usuario

        Raises:
            JWTError: Si el token es inválido
        """
        payload = TokenManager.verify_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise JWTError("Token no contiene user_id")
        return user_id

    @staticmethod
    def get_username_from_token(token: str) -> str:
        """
        Obtener el nombre de usuario desde un token JWT

        Args:
            token: Token JWT

        Returns:
            Nombre de usuario

        Raises:
            JWTError: Si el token es inválido
        """
        payload = TokenManager.verify_token(token)
        username = payload.get("sub")
        if not username:
            raise JWTError("Token no contiene nombre de usuario")
        return username
