from pathlib import Path
import cv2


VIDEO_PATH = Path("outputs/videos/m3_narrative_demo.mp4")

OUTPUTS = {
    "narrative": Path("docs/assets/m3/narrative/m3_narrative_sample.jpg"),
    "dashboard": Path("docs/assets/m3/dashboard/dashboard_sample.jpg"),
    "ghost_basic": Path("docs/assets/m3/ghost_replay/ghost_basic_sample.jpg"),
    "ghost_smart": Path("docs/assets/m3/ghost_replay/ghost_smart_sample.jpg"),
    "emotional_colors": Path("docs/assets/m3/emotional_colors/emotional_colors_sample.jpg"),
    "emotional_memory": Path("docs/assets/m3/emotional_memory/memory_sample.jpg"),
    "tactical_map": Path("docs/assets/m3/tactical_map/tactical_map_sample.jpg"),
}


# Cambia estos segundos según donde se vea mejor cada cosa
SAMPLES_SECONDS = {
    "narrative": 1.0,
    "dashboard": 1.0,
    "ghost_basic": 1.0,
    "ghost_smart": 1.0,
    "emotional_colors": 1.0,
    "emotional_memory": 1.0,
    "tactical_map": 1.0,
}


def extract_frame(video_path, second):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise FileNotFoundError(f"No se pudo abrir el video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_index = int(second * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError(f"No se pudo extraer el frame en segundo {second}")

    return frame


def save_image(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    print(f"Guardado: {path}")


def main():
    for name, output_path in OUTPUTS.items():
        second = SAMPLES_SECONDS[name]
        frame = extract_frame(VIDEO_PATH, second)
        save_image(output_path, frame)


if __name__ == "__main__":
    main()