import os
import logging


def setup_logger(name=__name__, log_folder="log", log_file="app.log", level=logging.INFO):
    """
    Configura y retorna un logger que escribe en consola y en un archivo.

    :param name: Nombre del logger.
    :param log_folder: Carpeta donde se guardará el archivo de log.
    :param log_file: Nombre del archivo de log.
    :param level: Nivel de logging.
    :return: Logger configurado.
    """
    # Asegurarse de que la carpeta de logs exista
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Ruta completa del archivo de log
    log_path = os.path.join(log_folder, log_file)

    # Crear el logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formateador
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Handler para el archivo
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Handler para la consola
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    # Evitar que se agreguen múltiples handlers si ya existen
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
