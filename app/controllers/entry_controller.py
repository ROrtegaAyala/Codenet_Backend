from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.entry_service import EntryService
from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear un espacio de nombres (namespace) para las entradas de blog
entry_ns = Namespace('entries', description='Operaciones relacionadas con las entradas de blog')

# Modelo de entrada para entradas de blog
entry_model = entry_ns.model('Entry', {
    'cover_img': fields.String(description='Imagen de portada'),
    'title': fields.String(description='Título de la entrada'),
    'description': fields.String(description='Descripción corta de la entrada'),
    'content': fields.String(description='Contenido principal de la entrada de blog'),
    'category': fields.String(description='Categoría del contenido publicado'),
    'source_file': fields.String(description='Archivo de código fuente'),
    'github_link': fields.String(description='Enlace al repositorio de github'),
})

# Modelo de salida para entradas de blog (respuesta)
entry_response_model = entry_ns.model('EntryResponse', {
    'id_entry': fields.Integer(description='ID de la entrada de blog'),
    'cover_img': fields.String(description='Imagen de portada'),
    'title': fields.String(description='Título de la entrada'),
    'description': fields.String(description='Descripción corta de la entrada'),
    'content': fields.String(description='Contenido principal de la entrada de blog'),
    'category': fields.String(description='Categoría del contenido publicado'),
    'source_file': fields.String(description='Archivo de código fuente'),
    'github_link': fields.String(description='Enlace al repositorio de github'),
    'created_at': fields.DateTime(description='Fecha de creación de la entrada'),
    'author': fields.String(attribute='user.name', description='Nombre del autor de la entrada'),
})

# Definir el controlador de entradas de blog con decoradores para la documentación
@entry_ns.route('/')
class EntryResource(Resource):
    @jwt_required()
    @entry_ns.doc('create_entry')
    @entry_ns.expect(entry_model, validate=True)  # Decorador para esperar el modelo en la petición
    @entry_ns.marshal_with(entry_response_model, code=201)  # Serialización automática de la entrada creada
    def post(self):
        """
        Crear una nueva entrada de blog
        ---
        Este método permite crear una nueva entrada de blog proporcionando como mínimo la imagen de portada,
        el título, el contenido, la categoría y el usuario. 
        
        Body Parameters:
        - cover_img: Imagen de portada
        - title: Título de la entrada
        - description: Descripción corta de la entrada - resumen. 
        - category: Categoría del contenido de la entrada de blog.
        - source_file: archivo de código fuente
        - github_link: link del repositorio de github
        - created_at: Fecha de creación de la entrada.
        - id_user: ID del usuario asociado

        Responses:
        - 201: Entrada de blog creada con éxito.
        - 400: Si ocurre un error durante la creación de la entrada de blog.
        """
        id_user = get_jwt_identity() #Obtiene el id_user del JWT
        print(f"id_user from JWT: {id_user}")
        data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud
        
        # Validación de campos requeridos para creación
        required_fields = ['cover_img', 'title', 'content', 'category']
        for field in required_fields:
            if field not in data: 
                return jsonify({'error': f'El campo {field} es requerido'}), 400
            
        entry = EntryService.create_entry(data, id_user)
        # Usamos jsonify para asegurarnos de que la respuesta siga el formato JSON válido.
        # return jsonify({'message': 'Entry created successfully', 'Entry': entry.title})
        return entry

    @entry_ns.doc('get_entries')
    @entry_ns.marshal_list_with(entry_response_model)  # Serialización automática de la lista de entradas
    def get(self):
        """
        Obtener todas las entradas de blog
        ---
        Este método permite obtener una lista de todas las entradas de blog registradas en la base de datos.

        Responses:
        - 200: Retorna una lista de títulos de entrada de blog (se podrá desplegar toda la info de cada entrada?).
        """
        entries = EntryService.get_all_entries()  # Llama al servicio para obtener todas las entradas
        # Usamos jsonify para garantizar que la lista de entradas se retorne como un JSON válido.
        # return jsonify({'entries': [entry.title for entry in entries]})  # Retorna solo los títulos de las entradas
        return entries


@entry_ns.route('/<id_entry>')
@entry_ns.param('id_entry', 'El ID de la entrada de blog')
class EntryDetailResource(Resource):
    @jwt_required()
    @entry_ns.doc('delete_entry')
    def delete(self, id_entry):
        """
        Eliminar una entrada de blog
        ---
        Este método permite eliminar una entrada existente basado en el ID.

        Path Parameters:
        - id_entry: El ID de la entrada de blog a eliminar.

        Responses:
        - 200: Entrada de blog eliminada con éxito.
        - 404: Si la entrada de blog no se encuentra.
        """

        id_user = get_jwt_identity() # Obtiene el ID del usuario autor autenticado
        entry = EntryService.get_entry_by_id(id_entry)

        # Verifica si la entrada existe y pertenece al usuario autenticado
        if entry.id_user != id_user:
            return jsonify({'message': "You're not authorized to delete this blog entry"}), 403
        EntryService.delete_entry(id_entry)  # Llama al servicio para eliminar la entrada
        # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
        return jsonify({'message': 'Entry deleted successfully'})

    @jwt_required()
    @entry_ns.doc('update_entry')
    @entry_ns.expect(entry_model, validate=True)
    @entry_ns.marshal_with(entry_response_model, code=201)  # Serialización automática de la entrada actualizada
    def put(self, id_entry):
        """
        Actualizar una entrada de blog
        ---
        Este método permite actualizar la información de una entrada de blog basado en su ID.

        Path Parameters:
        - id_entry: El ID de la entrada de blog que se actualizará.

        Body Parameters:
        - cover_img: La nueva imagen de portada (opcional).
        - title: El nuevo título (opcional).
        - description: La nueva descripción de la entrada (opcional).
        - content: El nuevo contenido de la entrada (opcional).
        - category: La nueva categoría (opcional).
        - source_file: El nuevo archivo de código fuente (opcional).
        - github_link: El nuevo link del repositorio (opcional).

        Responses:
        - 200: Entrada actualizada con éxito.
        - 404: Si la entrada no se encuentra.
        """
        id_user = get_jwt_identity() # Obtiene el ID del usuario autenticado

        #Verificar si la entrada existe y pertenece al usuario autenticado
        entry = EntryService.get_entry_by_id(id_entry)
        if entry.id_user != id_user:
            return jsonify({'message': "You're not authorized to update this blog entry"}), 403
        new_data = request.get_json()  # Obtiene los nuevos datos para la actualización
        updated_entry = EntryService.update_entry(id_entry, new_data)  # Llama al servicio para actualizar la entrada

        # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
        #return jsonify({'message': 'Entry updated successfully', 'Entry': entry}, 200)
        return updated_entry, 200

