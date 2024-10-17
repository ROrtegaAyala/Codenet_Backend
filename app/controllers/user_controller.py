from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear un espacio de nombres (namespace) para los usuarios
user_ns = Namespace('users', description='Operaciones relacionadas con los usuarios')

# Modelo de entrada para usuarios
user_model = user_ns.model('User', {
    'email': fields.String(description='Correo electrónico del usuario'),
    'password': fields.String(description='Contraseña del usuario'),
    'username': fields.String(description='Nombre de usuario de identificación'),
    'name': fields.String(description='Nombre del usuario'),
    'bio': fields.String(description='Biografía del usuario'),
    'profile_pic': fields.String(description='Foto de perfil del usuario')
})

# Modelo de salida (respuesta) para usuarios
user_response_model = user_ns.model('UserResponse', {
    'id_user': fields.Integer(description='ID del usuario'),
    'email': fields.String(description='Correo electrónico del usuario'),
    'password': fields.String(description='Contraseña del usuario'),
    'username': fields.String(description='Nombre de usuario de identificación'),
    'name': fields.String(description='Nombre del usuario'),
    'bio': fields.String(description='Biografía del usuario'),
    'profile_pic': fields.String(description='Foto de perfil del usuario'),
    'member_since': fields.String(description='Fecha en que el usuario se unió al sistema'),
})

# Definir el controlador de usuarios con decoradores para la documentación
@user_ns.route('/')
class UserResource(Resource):
    @user_ns.doc('create_user')
    @user_ns.expect(user_model, validate=True)  # Decorador para esperar el modelo en la petición
    @user_ns.marshal_with(user_response_model, code=201)  # Serialización automática del usuario creado
    def post(self):
        """
        Crear un nuevo usuario
        ---
        Este método permite crear un nuevo usuario proporcionando los datos requeridos.

        Body Parameters:
        - email: El correo electrónico del usuario a crear.
        - password: La contraseña del usuario.
        - username: El nombre de usuario.
        - name: El nombre completo del usuario.
        - bio: Biografía del usuario (opcional).
        - profile_pic: Foto de perfil del usuario (opcional).
        - member_since: Fecha de registro del usuario (opcional).

        Responses:
        - 201: Usuario creado con éxito.
        - 400: Si ocurre un error durante la creación del usuario.
        """
        data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud

        # Validación de campos requeridos para creación
        required_fields = ['email', 'username', 'password']
        for field in required_fields:
            if field not in data: 
                return jsonify({'error': f'El campo {field} es requerido'}), 400

        user = UserService.create_user(data)
        # Usamos jsonify para asegurarnos de que la respuesta siga el formato JSON válido.
        #return jsonify({'message': 'User created successfully', 'user': user.username})
        return user

    @user_ns.doc('get_users')
    def get(self):
        """
        Obtener todos los usuarios
        ---
        Este método permite obtener una lista de todos los usuarios registrados en la base de datos.

        Responses:
        - 200: Retorna una lista de nombres de usuarios.
        """
        users = UserService.get_all_users()  # Llama al servicio para obtener todos los usuarios
        # Usamos jsonify para garantizar que la lista de usuarios se retorne como un JSON válido.
        return jsonify({'users': [user.username for user in users]})  # Retorna solo los nombres de usuario


@user_ns.route('/<username>')
@user_ns.param('username', 'El nombre de usuario')
class UserDetailResource(Resource):
    @jwt_required()
    @user_ns.doc('delete_user')
    def delete(self, username):
        """
        Eliminar un usuario
        ---
        Este método permite eliminar un usuario existente basado en el nombre de usuario.

        Path Parameters:
        - username: El nombre del usuario a eliminar.

        Responses:
        - 200: Usuario eliminado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        id_user = get_jwt_identity() # Obtiene el ID del usuario autenticado
        user = UserService.get_user_by_username(username)

        # Verifica si el usuario existe y pertenece al usuario autenticado
        if user.id_user != id_user:
            return jsonify({'message': "You're not authorized to delete this user"}), 403
        
        UserService.delete_user(username)  # Llama al servicio para eliminar al usuario
        # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
        return jsonify({'message': 'User deleted successfully'})

    @jwt_required()
    @user_ns.doc('update_user')
    @user_ns.expect(user_model, validate=True)
    @user_ns.marshal_with(user_response_model, code=201)  # Serialización automática del usuario actualizado
    def put(self, username):
        """
        Actualizar un usuario
        ---
        Este método permite actualizar la información de un usuario basado en su nombre de usuario.

        Path Parameters:
        - username: El nombre del usuario que se actualizará.

        Body Parameters:
        - email: El nuevo correo electrónico del usuario (opcional).
        - password: La nueva contraseña del usuario (opcional).
        - username: El nuevo nombre de usuario (opcional).
        - name: El nuevo nombre completo del usuario (opcional).
        - bio: Nueva biografía del usuario (opcional).
        - profile_pic: Nueva foto de perfil del usuario (opcional).
        - member_since: Nueva fecha de registro del usuario (opcional).

        Responses:
        - 200: Usuario actualizado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        id_user = get_jwt_identity() #Obtiene el ID del usuario autenticado
        user = UserService.get_user_by_username(username)

        #Verifica si el usuario existe y pertenece al usuario autenticado
        if user.id_user != id_user:
            return jsonify({'message': "You're not authorized to update this user"}), 403
        
        new_data = request.get_json()  # Obtiene los nuevos datos para la actualización
        updated_user = UserService.update_user(username, new_data)  # Llama al servicio para actualizar el usuario
        # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
        # return jsonify({'message': 'User updated successfully'})
        return updated_user, 200