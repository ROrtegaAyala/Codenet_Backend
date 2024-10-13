from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from app.services.user_service import UserService

def login_required(func):
    """
    Middleware personalizado para verificar si el usuario está autenticado.

    Returns:
        Función decoradora que protege el endpoint y restringe el acceso si el usuario no está autenticado.
    """
    @wraps(func)  # Mantiene el nombre y la docstring original de la función decorada
    def wrapper(*args, **kwargs):
        # Obtener el email del usuario autenticado a partir del token JWT
        email = get_jwt_identity()
        
        # Buscar el usuario en la base de datos por su email
        user = UserService.get_user_by_email(email)
        
        # Verificar si el usuario existe
        if not user:
            # Si el usuario no está autenticado, se retorna un mensaje de error y un código de estado 401
            return jsonify({"message": "Usuario no autenticado"}), 401
        
        # Si el usuario está autenticado, continuar con la ejecución del endpoint
        return func(*args, **kwargs)
    
    return wrapper  # Retorna la función decorada con las verificaciones de autenticación
