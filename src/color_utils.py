"""
Utilidades HSV para Echomain.

Este módulo NO reemplaza a SAM 3. Sirve como apoyo para clasificar por color
los objetos ya segmentados/rastreados: robot azul, robot rojo y balón naranja.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
import pandas as pd


# En OpenCV, H va de 0 a 179. Estos rangos son iniciales y deben ajustarse
# con frames reales si la iluminación cambia.
HSV_RANGES: dict[str, list[tuple[np.ndarray, np.ndarray]]] = {
    "blue": [
        (np.array([90, 55, 35]), np.array([132, 255, 255])),
    ],
    "red": [
        (np.array([0, 55, 35]), np.array([12, 255, 255])),
        (np.array([168, 55, 35]), np.array([179, 255, 255])),
    ],
    "orange": [
        (np.array([5, 70, 70]), np.array([28, 255, 255])),
    ],
}


def create_color_mask(bgr_image: np.ndarray, color_name: str) -> np.ndarray:
    """Crea una máscara binaria para un color usando HSV."""
    if color_name not in HSV_RANGES:
        raise ValueError(f"Color no soportado: {color_name}. Usa {list(HSV_RANGES)}")

    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    final_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for lower, upper in HSV_RANGES[color_name]:
        mask = cv2.inRange(hsv, lower, upper)
        final_mask = cv2.bitwise_or(final_mask, mask)

    return final_mask


def color_ratio(
    bgr_image: np.ndarray,
    color_name: str,
    object_mask: np.ndarray | None = None,
) -> float:
    """Calcula la proporción de pixeles de un color en una región."""
    if bgr_image.size == 0:
        return 0.0

    color_mask = create_color_mask(bgr_image, color_name)

    if object_mask is not None:
        object_mask_uint8 = (object_mask.astype(np.uint8) * 255)
        object_mask_uint8 = cv2.resize(
            object_mask_uint8,
            (bgr_image.shape[1], bgr_image.shape[0]),
            interpolation=cv2.INTER_NEAREST,
        )
        color_mask = cv2.bitwise_and(color_mask, object_mask_uint8)
        total_pixels = int(np.count_nonzero(object_mask_uint8))
    else:
        total_pixels = int(bgr_image.shape[0] * bgr_image.shape[1])

    if total_pixels <= 0:
        return 0.0

    return float(np.count_nonzero(color_mask) / total_pixels)


def bbox_from_track_row(row: pd.Series) -> tuple[int, int, int, int]:
    """Convierte centro/ancho/alto del CSV en bbox xyxy."""
    x_center = float(row["x_center"])
    y_center = float(row["y_center"])
    width = float(row["width"])
    height = float(row["height"])

    x1 = int(round(x_center - width / 2))
    y1 = int(round(y_center - height / 2))
    x2 = int(round(x_center + width / 2))
    y2 = int(round(y_center + height / 2))
    return x1, y1, x2, y2


def crop_bbox(frame: np.ndarray, bbox: Iterable[int]) -> np.ndarray:
    """Recorta un bbox asegurando límites válidos."""
    x1, y1, x2, y2 = [int(v) for v in bbox]
    h, w = frame.shape[:2]

    x1 = max(0, min(w - 1, x1))
    x2 = max(0, min(w, x2))
    y1 = max(0, min(h - 1, y1))
    y2 = max(0, min(h, y2))

    if x2 <= x1 or y2 <= y1:
        return np.empty((0, 0, 3), dtype=frame.dtype)

    return frame[y1:y2, x1:x2]


def classify_object_color(
    frame: np.ndarray,
    bbox: Iterable[int],
    min_score: float = 0.04,
) -> tuple[str, float]:
    """Clasifica un objeto por color dominante dentro de su bounding box."""
    crop = crop_bbox(frame, bbox)

    if crop.size == 0:
        return "unknown", 0.0

    ratios = {
        "blue": color_ratio(crop, "blue"),
        "red": color_ratio(crop, "red"),
        "orange": color_ratio(crop, "orange"),
    }

    best_color = max(ratios, key=ratios.get)
    best_score = float(ratios[best_color])

    if best_score < min_score:
        return "unknown", best_score

    return best_color, best_score


def color_to_team(color_name: str, class_name: str = "") -> str:
    """Convierte color dominante en etiqueta de equipo/tipo."""
    class_name = str(class_name).lower()

    if "ball" in class_name or color_name == "orange":
        return "ball"
    if color_name == "blue":
        return "blue"
    if color_name == "red":
        return "red"
    return "unknown"


def classify_tracks_with_hsv(
    video_path: str | Path,
    tracks_csv: str | Path,
    output_csv: str | Path,
    min_score: float = 0.04,
    max_frames: int | None = None,
) -> pd.DataFrame:
    """
    Lee un video y un CSV de tracking para agregar columnas HSV:
    color, color_score y team.

    El CSV debe tener: frame, class_name, x_center, y_center, width, height.
    """
    video_path = Path(video_path)
    tracks_csv = Path(tracks_csv)
    output_csv = Path(output_csv)

    if not video_path.exists():
        raise FileNotFoundError(f"No existe el video: {video_path}")
    if not tracks_csv.exists():
        raise FileNotFoundError(f"No existe el CSV: {tracks_csv}")

    df = pd.read_csv(tracks_csv)

    required = {"frame", "x_center", "y_center", "width", "height"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en tracks CSV: {sorted(missing)}")

    df["color"] = "unknown"
    df["color_score"] = 0.0
    df["team"] = "unknown"

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {video_path}")

    frames_needed = set(df["frame"].astype(int).unique().tolist())
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if max_frames is not None and frame_idx > max_frames:
            break

        if frame_idx in frames_needed:
            idxs = df.index[df["frame"].astype(int) == frame_idx].tolist()
            for idx in idxs:
                row = df.loc[idx]
                bbox = bbox_from_track_row(row)
                color, score = classify_object_color(frame, bbox, min_score=min_score)
                class_name = str(row.get("class_name", ""))

                df.at[idx, "color"] = color
                df.at[idx, "color_score"] = score
                df.at[idx, "team"] = color_to_team(color, class_name)

        frame_idx += 1

    cap.release()

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    return df
