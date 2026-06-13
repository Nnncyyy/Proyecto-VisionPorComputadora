from pathlib import Path
import cv2
import pandas as pd


VIDEO_PATH = Path("data/raw/videoInstrucciones.mov")
CSV_PATH = Path("outputs/metrics/tracks_with_color.csv")
OUTPUT_PATH = Path("docs/assets/m3/hsv/hsv_sample.jpg")


def get_best_frame(df: pd.DataFrame) -> int:
    """
    Busca un frame donde haya más objetos con color detectado.
    """
    valid = df[df["color"].notna() & (df["color"] != "unknown")]

    if len(valid) == 0:
        print("No se encontraron colores válidos. Usando el primer frame disponible.")
        return int(df["frame"].iloc[0])

    frame_counts = valid.groupby("frame").size().sort_values(ascending=False)
    return int(frame_counts.index[0])


def read_frame(video_path: Path, frame_index: int):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise FileNotFoundError(f"No se pudo abrir el video: {video_path}")

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError(f"No se pudo leer el frame {frame_index}")

    return frame


def color_bgr(color_name: str):
    """
    Colores para visualizar etiquetas HSV.
    """
    if color_name == "blue":
        return (255, 80, 40)
    if color_name == "red":
        return (40, 40, 255)
    if color_name == "orange":
        return (0, 165, 255)
    return (255, 255, 255)


def draw_hsv_labels(frame, frame_df: pd.DataFrame):
    output = frame.copy()

    for _, row in frame_df.iterrows():
        x = int(row["x_center"])
        y = int(row["y_center"])

        width = int(row.get("width", 40))
        height = int(row.get("height", 40))

        x1 = max(0, int(x - width / 2))
        y1 = max(0, int(y - height / 2))
        x2 = min(output.shape[1] - 1, int(x + width / 2))
        y2 = min(output.shape[0] - 1, int(y + height / 2))

        class_name = str(row.get("class_name", "object"))
        color = str(row.get("color", "unknown"))
        team = str(row.get("team", "unknown"))
        score = float(row.get("color_score", 0.0))

        draw_color = color_bgr(color)

        cv2.rectangle(output, (x1, y1), (x2, y2), draw_color, 2)
        cv2.circle(output, (x, y), 5, draw_color, -1)

        label = f"{class_name} | {color} | {team} | {score:.2f}"

        cv2.putText(
            output,
            label,
            (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            draw_color,
            2,
            cv2.LINE_AA,
        )

    return output


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"No existe {CSV_PATH}. Primero ejecuta main_m3.py para generar tracks_with_color.csv"
        )

    df = pd.read_csv(CSV_PATH)

    required_columns = {"frame", "x_center", "y_center", "color", "team", "color_score"}

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {missing}")

    frame_index = get_best_frame(df)

    print(f"Frame seleccionado para evidencia HSV: {frame_index}")

    frame = read_frame(VIDEO_PATH, frame_index)

    frame_df = df[df["frame"] == frame_index].copy()

    hsv_sample = draw_hsv_labels(frame, frame_df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUTPUT_PATH), hsv_sample)

    print(f"Evidencia HSV guardada en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()