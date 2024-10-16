from datetime import datetime
from app.models.user import User
from app import db

class UserService:
    @staticmethod
    def create_user(email, password, username, name, bio=None, profile_pic=None, member_since=None):
        # Crear una nueva instancia del usuario con los datos proporcionados
        new_user = User(
            email=email,
            password=password,
            username=username,
            name=name,
            bio=bio,
            profile_pic=profile_pic,
            member_since=member_since
        )
        # Agregar el nuevo usuario a la sesión de la base de datos y confirmar los cambios
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @staticmethod
    def get_all_users():
        """
        Obtener todos los usuarios de la base de datos.
        
        Returns:
            List[User]: Lista de todos los usuarios en la base de datos.
        """
        # Recuperar todos los registros de la tabla User
        return User.query.all()

    @staticmethod
    def get_user_by_username(username):
        """
        Obtener un usuario por su nombre de usuario.
        
        Args:
            username (str): Nombre de usuario a buscar.
        
        Returns:
            User: El usuario encontrado o None si no existe.
        """
        # Filtrar usuarios por su nombre de usuario (username)
        return User.query.filter_by(username=username).first()

    @staticmethod
    def update_user(user_id, email=None, password=None, username=None, name=None, bio=None, profile_pic=None):
        # Buscar el usuario por su ID
        user = User.query.get(user_id)
        if not user:
            return None

        # Actualizar los campos del usuario solo si se proporcionan nuevos valores
        if email:
            user.email = email
        if password:
            user.password = password
        if username:
            user.username = username
        if name:
            user.name = name
        if bio:
            user.bio = bio
        if profile_pic:
            user.profile_pic = profile_pic

        # Confirmar los cambios en la base de datos
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        # Buscar el usuario por su ID
        user = User.query.get(user_id)
        if not user:
            return False

        # Eliminar el usuario de la base de datos y confirmar los cambios
        db.session.delete(user)
        db.session.commit()
        return True
