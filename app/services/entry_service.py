from app import db, bcrypt
from app.models.entry import Entry
from app.models.user import User

class EntryService:
    @staticmethod
    def create_entry(data, id_user):
        """
        Crear una nueva entrada de blog con un usuario asignado.
        
        Args:
            cover_img (blob/string): Imagen de portada
            title (str): Título de la entrada
            description (str): Descripción corta de la entrada - resumen. 
            category (str): Categoría de la entrada de blog.
            source_file (MEDIUMBLOB/str): archivo de código fuente
            github_link (str): link del repositorio de github
            created_at (datetime): Fecha de creación de la entrada.
            id_user (int): ID del usuario asociado
        
        Returns:
            Entry: La entrada de blog creada.
        
        Raises:
            ValueError: Si el usuario asociado no es encontrado.
        """
        # Buscar el rol asociado al usuario por su ID
        user = User.query.filter_by(id_user=id_user).first()
        if not user:
            # Si no se encuentra el usuario, lanzar una excepción
            raise ValueError('User not found')
        
        # Crear un nuevo objeto Entry con el usuario asociado
        entry_data = {**data, 'id_user': id_user}
        entry = Entry(**entry_data)
        
        # Añadir la nueva entrada a la base de datos
        db.session.add(entry)
        db.session.commit()
        
        return entry  # Retornar la entrada recién creada
    
    @staticmethod
    def get_all_entries():
        """
        Obtener todas las entradas de blog de la base de datos.
        
        Returns:
            List[Entry]: Lista de todas las entradas de blog en la base de datos.
        """
        # Recuperar todos los registros de la tabla User
        return Entry.query.all()

    @staticmethod
    def get_entry_by_id(id_entry):
        """
        Obtener una entrada de blog por su id.
        
        Args:
            id (int): Id de entrada de blog a buscar.
        
        Returns:
            Entry: La entrada de blog encontrada o None si no existe.
        """
        # Filtrar entradas de blog por su id (id_entry)
        return Entry.query.filter_by(id_entry=id_entry).first()

    @staticmethod
    def update_entry(id_entry, new_data):
        """
        Actualizar los datos de una entrada de blog existente.
        
        Args:
            id_entry (int): ID de la entrada de blog a actualizar.
            new_data (dict): Diccionario con los nuevos datos, como 'category' o 'content'.
        
        Returns:
            None
        
        Raises:
            ValueError: Si la entrada de blog no es encontrada.
        """
        # Buscar al usuario por su nombre de usuario
        entry = EntryService.get_entry_by_id(id_entry)
        if not entry:
            # Si no se encuentra la entrada, lanzar una excepción
            raise ValueError('Blog Entry not found')
        
        # Actualiza los atributos del objeto de entrada
        for key, value in new_data.items():
            if hasattr(entry, key): #Verifica si el atributo existe en el objeto
                setattr(entry, key, value)

        # Guardar los cambios en la base de datos
        db.session.commit()
        return entry

    @staticmethod
    def delete_entry(id_entry):
        """
        Eliminar una entrada de blog existente.
        
        Args:
            id_entry (int): ID de la entrada de blog a eliminar.
        
        Returns:
            None
        
        Raises:
            ValueError: Si la entrada de blog no es encontrada.
        """
        # Buscar la entrada de blog por su ID
        entry = EntryService.get_entry_by_id(id_entry)
        if not entry:
            # Si no se encuentra la entrada, lanzar una excepción
            raise ValueError('Blog entry not found')

        # Eliminar la entrada de la base de datos
        db.session.delete(entry)
        db.session.commit()
