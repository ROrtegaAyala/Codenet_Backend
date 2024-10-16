from datetime import datetime
from app.models.user import User
from app import db, bcrypt

class UserService:
    @staticmethod
    def create_user(email, password, username, name, bio=None, profile_pic=None, member_since=None):
        # Crear una nueva instancia del usuario con los datos proporcionados
        new_user = User(
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
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
    def update_user(username, newdata):
        # Buscar el usuario por su ID
        user = UserService.get_user_by_username(username)
        if not user:
            # Si no se encuentra el usuario, lanzar una excepción
            raise ValueError('User not found')

        # Actualizar los campos del usuario solo si se proporcionan nuevos valores
        if 'username' in newdata:
            existing_user = User.query.filter_by(username=newdata['username']).first()
            if existing_user:
                # Si se encuentra un usuario existente, lanzar una excepción
                raise ValueError('Username already exists')
            user.username = newdata['username']

        if 'email' in newdata:
            existing_email = User.query.filter_by(email=newdata['email']).first()
            if existing_email:
                # Si se encuentra un usuario existente, lanzar una excepción
                raise ValueError('Email already linked to an account')
            user.email = newdata['email']

        if 'password' in newdata:
            user.password = bcrypt.generate_password_hash(newdata['password']).decode('utf-8')

        # Confirmar los cambios en la base de datos
        db.session.commit()
        return user

    @staticmethod
    def delete_user(username):
        # Buscar el usuario por su ID
        user = UserService.get_user_by_username(username)
        if not user:
            # Si no se encuentra el usuario, lanzar una excepción
            raise ValueError('User not found')

        # Eliminar el usuario de la base de datos y confirmar los cambios
        db.session.delete(user)
        db.session.commit()
        return True
