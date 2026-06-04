import os

# Rutas base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Rutas específicas
MODEL_PATH = os.path.join(ASSETS_DIR, "sam3.pt")