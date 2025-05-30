import os
import importlib

# Ruta al directorio que contiene los modelos
modelos_dir = os.path.dirname(__file__)

# Itera sobre todos los archivos del directorio de modelos
for filename in os.listdir(modelos_dir):
    # Verifica si el archivo es un archivo .py y no es __init__.py
    if filename.endswith('.py') and filename != '__init__.py':
        # Importa el módulo usando su nombre de archivo (sin la extensión .py)
        module_name = f'blog.Models.{filename[:-3]}'
        importlib.import_module(module_name)