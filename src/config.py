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
# Salidas y assets de M3
M3_DOCS_ASSETS_DIR = DOCS_DIR / "assets" / "m3"
M3_HSV_DIR = M3_DOCS_ASSETS_DIR / "hsv"
M3_GHOST_DIR = M3_DOCS_ASSETS_DIR / "ghost_replay"
M3_HOMOGRAPHY_DIR = M3_DOCS_ASSETS_DIR / "homography"
M3_TACTICAL_MAP_DIR = M3_DOCS_ASSETS_DIR / "tactical_map"
M3_HEATMAP_DIR = M3_DOCS_ASSETS_DIR / "heatmap"
M3_DASHBOARD_DIR = M3_DOCS_ASSETS_DIR / "dashboard"
M3_NARRATIVE_DIR = M3_DOCS_ASSETS_DIR / "narrative"

OUTPUT_TRACKS_COLOR_CSV = OUTPUTS_DIR / "metrics" / "tracks_with_color.csv"
OUTPUT_TRACKS_PROJECTED_CSV = OUTPUTS_DIR / "metrics" / "tracks_projected.csv"
OUTPUT_EMOTIONS_CSV = OUTPUTS_DIR / "metrics" / "emotions.csv"
OUTPUT_EVENTS_CSV = OUTPUTS_DIR / "metrics" / "events.csv"
OUTPUT_M3_VIDEO = OUTPUTS_DIR / "videos" / "m3_narrative_demo.mp4"
