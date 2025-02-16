import os
from flask import Flask, jsonify, request
from resources.Config import Config
from controls.Auth_Control import auth_bp, google_bp
from controls.Pokemon_Control import pokemon_bp
from flask_jwt_extended import JWTManager
from log.Logger import setup_logger  # Importa la función para configurar el logger


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurar JWT usando la misma clave secreta definida en sensitive.properties
    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY
    JWTManager(app)

    # Configurar el logger
    logger = setup_logger()  # Se usará "log/app.log" en la carpeta log

    # Registrar un hook para loggear cada solicitud
    @app.before_request
    def log_request_info():
        logger.info("Solicitud: %s %s", request.method, request.url)

    # Registrar blueprints
    app.register_blueprint(google_bp, url_prefix="/login")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(pokemon_bp, url_prefix="/pokemon")

    @app.route("/")
    def index():
        return ("Bienvenido a la Biblioteca de Pokémon. "
                "Autentícate y obtén tu token JWT.")

    # Manejador global de errores: registra excepciones
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("Ocurrió una excepción: %s", e)
        return jsonify({"msg": "Ocurrió un error interno. Por favor, inténtalo más tarde."}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    # Usar ssl_context con tus archivos generados
    app.run(debug=True, ssl_context=('ssl/cert.pem', 'ssl/key.pem'))

