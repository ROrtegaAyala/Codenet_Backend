from datetime import datetime
from app import db

class User(db.Model):
    """
    Modelo que representa un usuario en el sistema.

    Cada usuario tiene un correo electrónico, una contraseña encriptada, un nombre de usuario, 
    un nombre, una biografía, una foto de perfil y una fecha de creación.

    Atributos:
        id_user (int): Identificador único del usuario (clave primaria).
        email (str): Correo electrónico del usuario, debe ser único.
        password (str): Contraseña encriptada del usuario.
        username (str): Nombre de usuario.
        name (str): Nombre completo del usuario.
        bio (str): Biografía del usuario.
        profile_pic (blob): Foto de perfil del usuario.
        member_since (date): Fecha en que el usuario se unió al sistema.
    """

    __tablename__ = 'users'  # Especifica el nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id_user = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    email = db.Column(db.String(30), unique=True, nullable=False)  # Correo electrónico, debe ser único y no nulo
    password = db.Column(db.String(60), nullable=False)  # Contraseña encriptada del usuario, no puede ser nula
    username = db.Column(db.String(10), unique=True, nullable=False)  # Nombre de usuario, debe ser único y no nulo
    name = db.Column(db.String(50), nullable=False)  # Nombre completo del usuario
    bio = db.Column(db.String(300))  # Biografía del usuario
    profile_pic = db.Column(db.String(300))  # Foto de perfil del usuario
    member_since = db.Column(db.DateTime, default=datetime.now())  # Fecha en que el usuario se unió al sistema

    # Relación con el modelo entry (para habilitar eliminación en cascada)
    entries = db.relationship('Entry', backref='user', cascade='all, delete-orphan') #Configuración para eliminación en cascada

    def __init__(self, **kwargs):
        """
        Constructor de la clase User.

        Args:
            email (str): El correo electrónico del usuario.
            password (str): La contraseña encriptada.
            username (str): El nombre de usuario.
            name (str): El nombre completo del usuario.
            bio (str, opcional): La biografía del usuario.
            profile_pic (blob, opcional): La foto de perfil del usuario.
            member_since (date, opcional): La fecha de membresía del usuario.
        """
        for key, value in kwargs.items():
            if key == 'member_since':
                setattr(self, key, datetime.now())
            else:
                setattr(self, key, value) 
