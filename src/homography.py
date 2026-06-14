"""Homografía y proyección a mapa táctico 2D."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


def load_homography_points(json_path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    """
    Carga puntos desde JSON.

    Formato esperado:
    {
      "image_points": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],
      "map_points": [[0,0], [800,0], [800,500], [0,500]]
    }
    """
    json_path = Path(json_path)
    if not json_path.exists():
        raise FileNotFoundError(f"No existe el archivo de puntos: {json_path}")

    data = json.loads(json_path.read_text(encoding="utf-8"))
    image_points = np.array(data["image_points"], dtype=np.float32)
    map_points = np.array(data["map_points"], dtype=np.float32)

    if image_points.shape != (4, 2) or map_points.shape != (4, 2):
        raise ValueError("Se requieren exactamente 4 puntos de imagen y 4 puntos de mapa")

    return image_points, map_points


def compute_homography(image_points: np.ndarray, map_points: np.ndarray) -> np.ndarray:
    return cv2.getPerspectiveTransform(image_points.astype(np.float32), map_points.astype(np.float32))


def project_points(points_xy: np.ndarray, H: np.ndarray) -> np.ndarray:
    points_xy = np.asarray(points_xy, dtype=np.float32)
    if points_xy.ndim != 2 or points_xy.shape[1] != 2:
        raise ValueError("points_xy debe tener forma (N, 2)")
    points = points_xy.reshape(-1, 1, 2)
    projected = cv2.perspectiveTransform(points, H)
    return projected.reshape(-1, 2)


def project_tracks_to_map(df: pd.DataFrame, H: np.ndarray) -> pd.DataFrame:
    df = df.copy()
    points = df[["x_center", "y_center"]].astype(float).to_numpy()
    projected = project_points(points, H)
    df["x_map"] = projected[:, 0]
    df["y_map"] = projected[:, 1]
    return df


def save_projected_tracks(
    tracks_csv: str | Path,
    points_json: str | Path,
    output_csv: str | Path,
) -> pd.DataFrame:
    image_points, map_points = load_homography_points(points_json)
    H = compute_homography(image_points, map_points)
    df = pd.read_csv(tracks_csv)
    projected = project_tracks_to_map(df, H)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    projected.to_csv(output_csv, index=False)
    return projected


def create_points_template(output_json: str | Path, map_width: int = 800, map_height: int = 500) -> None:
    """Crea una plantilla JSON para que el equipo llene puntos reales."""
    output_json = Path(output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    template = {
        "image_points": [
            [100, 100],
            [700, 100],
            [750, 500],
            [80, 500],
        ],
        "map_points": [
            [0, 0],
            [map_width, 0],
            [map_width, map_height],
            [0, map_height],
        ],
        "nota": "Reemplaza image_points con las cuatro esquinas reales de la cancha en tu video.",
    }
    output_json.write_text(json.dumps(template, indent=2), encoding="utf-8")
