from pathlib import Path
import cv2
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

TRACKS_CSV = ROOT / "outputs" / "metrics" / "tracks.csv"
VIDEO_PATH = ROOT / "outputs" / "videos" / "m2_tracking_demo.mp4"

DOCS_M2 = ROOT / "docs" / "assets" / "m2"
SAMPLE_CSV = DOCS_M2 / "sample_tracks.csv"
TRACKING_IMG = DOCS_M2 / "tracking" / "tracking_sample.jpg"
TRAILS_IMG = DOCS_M2 / "trails" / "trails_sample.jpg"


def create_dirs() -> None:
    (DOCS_M2 / "tracking").mkdir(parents=True, exist_ok=True)
    (DOCS_M2 / "trails").mkdir(parents=True, exist_ok=True)


def create_csv_sample(max_rows: int = 50) -> None:
    if not TRACKS_CSV.exists():
        raise FileNotFoundError(
            f"No existe {TRACKS_CSV}. Primero ejecuta el pipeline M2."
        )

    df = pd.read_csv(TRACKS_CSV)

    if df.empty:
        raise ValueError("El archivo tracks.csv está vacío.")

    df.head(max_rows).to_csv(SAMPLE_CSV, index=False)
    print(f"CSV de muestra creado: {SAMPLE_CSV}")


def extract_evidence_frame(frame_number: int = 30) -> None:
    if not VIDEO_PATH.exists():
        raise FileNotFoundError(
            f"No existe {VIDEO_PATH}. Primero ejecuta el pipeline M2."
        )

    cap = cv2.VideoCapture(str(VIDEO_PATH))

    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {VIDEO_PATH}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        raise RuntimeError("El video no contiene frames válidos.")

    frame_number = min(frame_number, total_frames - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ok, frame = cap.read()
    cap.release()

    if not ok:
        raise RuntimeError(f"No se pudo leer el frame {frame_number}.")

    cv2.imwrite(str(TRACKING_IMG), frame)
    cv2.imwrite(str(TRAILS_IMG), frame)

    print(f"Imagen de tracking creada: {TRACKING_IMG}")
    print(f"Imagen de trails creada: {TRAILS_IMG}")


def main() -> None:
    create_dirs()
    create_csv_sample(max_rows=50)
    extract_evidence_frame(frame_number=30)
    print("Evidencia M2 generada correctamente.")


if __name__ == "__main__":
    main()