from pathlib import Path

# Raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[1]

# Directorios principales
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = BASE_DIR / "assets"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Archivos locales esperados
MODEL_PATH = ASSETS_DIR / "sam3.pt"
VIDEO_PATH = RAW_DATA_DIR / "video-1080_singular_display.mov"

# Salidas locales
OUTPUT_VIDEO_PATH = OUTPUTS_DIR / "videos" / "m2_tracking_demo.mp4"
OUTPUT_TRACKS_CSV = OUTPUTS_DIR / "metrics" / "tracks.csv"

# Evidencia ligera para GitHub
M2_DOCS_ASSETS_DIR = DOCS_DIR / "assets" / "m2"
M2_TRACKING_SAMPLE = M2_DOCS_ASSETS_DIR / "tracking" / "tracking_sample.jpg"
M2_TRAILS_SAMPLE = M2_DOCS_ASSETS_DIR / "trails" / "trails_sample.jpg"
M2_SAMPLE_TRACKS_CSV = M2_DOCS_ASSETS_DIR / "sample_tracks.csv"