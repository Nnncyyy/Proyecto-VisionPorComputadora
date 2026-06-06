import os
import sys
from pathlib import Path
import cv2

# --- PARCHE DE COMPATIBILIDAD DE RUTAS (Fuerza a Python a encontrar 'src') ---
ruta_actual = Path(__file__).resolve().parent  # Carpeta 'src'
raiz_proyecto = ruta_actual.parent             # Carpeta raíz 'Proyecto-VisionPorComputadora'

if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))
# ------------------------------------------------------------------------------

from src.video_utils import get_video_info, iter_video_frames, create_video_writer
from src.segmentation import load_sam3_text_predictor, segment_frame_with_prompts
from src.tracking import FutbotTracker
from src.visualization import draw_tracking_frame
from src.export import init_tracks_csv, append_tracks_to_csv

# --- CONFIGURACIÓN DE RUTAS ABSOLUTAS AUTOMÁTICAS ---
# Esto evita que el script falle sin importar desde dónde lo ejecutes
VIDEO_PATH = raiz_proyecto / "data" / "raw" / "videoInstrucciones.mov" # O .mov, asegúrate de la extensión
MODEL_PATH = raiz_proyecto / "src" / "models" / "sam3.pt"

OUTPUT_VIDEO = raiz_proyecto / "outputs" / "videos" / "m2_tracking_demo.mp4"
OUTPUT_CSV = raiz_proyecto / "outputs" / "metrics" / "tracks.csv"

MAX_FRAMES = 50
STRIDE = 1


def main():
    # Diagnóstico rápido en caso de fallo
    print(f"Buscando modelo en: {MODEL_PATH.resolve()}")
    print(f"Buscando video en: {VIDEO_PATH.resolve()}")

    if not VIDEO_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el video en: {VIDEO_PATH.resolve()}. "
            "Revisa si el nombre o la extensión (.mp4 / .mov) es la correcta."
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo en: {MODEL_PATH.resolve()}. "
            "Por favor, muévelo a esa ubicación exacta."
        )

    info = get_video_info(VIDEO_PATH)

    print("Video info:", info)

    writer = create_video_writer(
        output_path=OUTPUT_VIDEO,
        fps=info["fps"],
        width=info["width"],
        height=info["height"],
    )

    # Asegura que las carpetas de salida existan antes de escribir
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    init_tracks_csv(OUTPUT_CSV)

    predictor = load_sam3_text_predictor(
        model_path=str(MODEL_PATH),
        conf=0.25,
    )

    tracker = FutbotTracker()

    for frame_idx, frame in iter_video_frames(
        VIDEO_PATH,
        max_frames=MAX_FRAMES,
        stride=STRIDE,
    ):
        print(f"Procesando frame {frame_idx}")

        detections = segment_frame_with_prompts(
            predictor=predictor,
            frame=frame,
        )

        detections = tracker.update(detections)

        append_tracks_to_csv(
            csv_path=OUTPUT_CSV,
            frame_idx=frame_idx,
            detections=detections,
        )

        annotated = draw_tracking_frame(
            frame=frame,
            detections=detections,
        )

        writer.write(annotated)

    writer.release()

    print(f"Video generado con éxito en: {OUTPUT_VIDEO}")
    print(f"CSV generado con éxito en: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()