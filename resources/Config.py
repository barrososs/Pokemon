import os
import configparser

# Directorio actual de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_properties(filename: str) -> configparser.ConfigParser:
    """Carga un archivo de propiedades desde el directorio resources."""
    config = configparser.ConfigParser()
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{filename}' no se encontró en {BASE_DIR}")
    config.read(file_path)
    return config


# Cargar propiedades generales y sensibles
app_config = load_properties("application.properties")
sensitive_config = load_properties("sensitive.properties")


class Config:
    # Configuración sensible
    SECRET_KEY = sensitive_config.get('DEFAULT', 'SECRET_KEY')
    GOOGLE_OAUTH_CLIENT_ID = sensitive_config.get('DEFAULT', 'GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = sensitive_config.get('DEFAULT', 'GOOGLE_OAUTH_CLIENT_SECRET')

    # Configuración de la aplicación
    POKEAPI_URL = app_config.get('DEFAULT', 'POKEAPI_URL')
