from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_migrate import Migrate
from .config import Config

# Inicializamos las extensiones globalmente
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    """Función factory para crear la aplicación Flask y configurar sus componentes."""
    app = Flask(__name__)

    # Cargamos la configuración desde el archivo config.py
    app.config.from_object(Config)

    # Inicializamos las extensiones con la aplicación
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Configuración para JWT en Swagger
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Bearer token. Ejemplo: "Bearer {token}"'
        }
    }

    # Configuramos la API Flask-RESTX
    api = Api(
        app,
        title='Codenet API',
        version='1.0',
        description='API para gestión de usuarios, entradas, comentarios y seguimientos',
        authorizations=authorizations,
        security='Bearer'
    )

    # Importamos los controladores y namespaces
    from .controllers.user_controller import user_ns
    from .controllers.entry_controller import entry_ns
    from .controllers.auth_controller import auth_ns
    #from .controllers.comment_controller import comment_ns
    #from .controllers.following_controller import following_ns

    # Registramos los namespaces
    api.add_namespace(user_ns, path='/users')
    api.add_namespace(entry_ns, path='/entries')
    api.add_namespace(auth_ns, path='/auth')
    #api.add_namespace(comment_ns, path='/comments')
    #api.add_namespace(following_ns, path='/followings')

    # Retornamos la aplicación ya configurada
    return app
