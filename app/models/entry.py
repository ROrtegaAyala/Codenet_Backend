from datetime import datetime
from app import db
from app.models.user import User


class Entry(db.Model):
    """
    Modelo que representa una entrada de blog en el sistema.

    Cada entrada de blog tiene un id, una imagen de portada, un título, una descripción,
    un contenido, una categoría, un archivo zip de código fuente, un link de repositorio 
    de github, una fecha de creación y está asociada a un usuario a través de una clave foránea.

    Atributos:
        id_entry (int): Identificador único de la entrada de blog (clave primaria).
        cover_img (blob/string): Imagen de portada
        title (str): Título de la entrada
        description (str): Descripción corta de la entrada - resumen. 
        category (str): Categoría de la entrada de blog.
        source_file (MEDIUMBLOB/str): archivo de código fuente
        github_link (str): link del repositorio de github
        created_at (datetime): Fecha de creación de la entrada.
        id_user (int): Relación con el modelo User que indica el autor de la entrada.
    """
    
    __tablename__ = 'entries'  # Especifica el nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id_entry = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    cover_img = db.Column(db.String(200), nullable=False) # Imagen de portada, no puede ser nula
    title = db.Column(db.String(100), nullable=False) # Título, no puede ser nulo
    description = db.Column(db.String(500)) # Descripción
    content = db.Column(db.String(200), nullable=False) # Contenido de la entrada, no puede ser nulo
    category = db.Column(db.String(15), nullable=False) # Categoría, no puede ser nula
    source_file = db.Column(db.String(100)) #Archivo de código fuente
    github_link = db.Column(db.String(100)) #Link al repositorio de github
    created_at = db.Column(db.DateTime, default=datetime.now()) # Fecha de creación de la entrada
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user', ondelete='CASCADE'), nullable=False) # Clave foránea hacia la tabla "users"

    # Relación con el modelo User
    # user = db.relationship('User', backref='entries') # Define la relación con el modelo User y permite acceso inverso desde User a Entry

    def __init__(self, **kwargs):
        """
        Constructor de la clase Entry.

        Args:
            cover_img (blob/string): Imagen de portada
            title (str): Título de la entrada
            description (str): Descripción corta de la entrada - resumen. 
            category (str): Categoría de la entrada de blog.
            source_file (MEDIUMBLOB/str): archivo de código fuente
            github_link (str): link del repositorio de github
            created_at (datetime): Fecha de creación de la entrada.
            id_user (int): ID del usuario asociado
        """
        for key, value in kwargs.items():
            if key == 'created_at':
                setattr(self, key, datetime.now())
            else:
                setattr(self, key, value)
