import cv2
import json
from pathlib import Path


VIDEO_PATH = Path("data/raw/videoInstrucciones.mov")
OUTPUT_PATH = Path("config/homography_points.json")

FRAME_INDEX = 30  # cambia este número si quieres otro frame

points = []


def mouse_callback(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append([x, y])
            print(f"Punto {len(points)}: [{x}, {y}]")


def get_frame(video_path, frame_index):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise FileNotFoundError(f"No se pudo abrir el video: {video_path}")

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError(f"No se pudo leer el frame {frame_index}")

    return frame


def draw_points(frame, points):
    img = frame.copy()

    for i, (x, y) in enumerate(points):
        cv2.circle(img, (x, y), 6, (0, 0, 255), -1)
        cv2.putText(
            img,
            str(i + 1),
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

    if len(points) == 4:
        pts = [(p[0], p[1]) for p in points]
        cv2.line(img, pts[0], pts[1], (0, 255, 0), 2)
        cv2.line(img, pts[1], pts[2], (0, 255, 0), 2)
        cv2.line(img, pts[2], pts[3], (0, 255, 0), 2)
        cv2.line(img, pts[3], pts[0], (0, 255, 0), 2)

    return img


def main():
    global points

    frame = get_frame(VIDEO_PATH, FRAME_INDEX)

    cv2.namedWindow("Selecciona 4 puntos de la cancha", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Selecciona 4 puntos de la cancha", mouse_callback)

    print("Instrucciones:")
    print("Haz clic en este orden:")
    print("1. esquina superior izquierda")
    print("2. esquina superior derecha")
    print("3. esquina inferior derecha")
    print("4. esquina inferior izquierda")
    print("")
    print("Teclas:")
    print("r = reiniciar puntos")
    print("s = guardar")
    print("q = salir")

    while True:
        display = draw_points(frame, points)
        cv2.imshow("Selecciona 4 puntos de la cancha", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            points = []
            print("Puntos reiniciados")

        elif key == ord("s"):
            if len(points) != 4:
                print("Debes seleccionar exactamente 4 puntos antes de guardar")
                continue

            data = {
                "image_points": points,
                "map_points": [
                    [0, 0],
                    [800, 0],
                    [800, 500],
                    [0, 500],
                ],
            }

            OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            print(f"Archivo guardado en: {OUTPUT_PATH}")
            print(json.dumps(data, indent=2))
            break

        elif key == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()