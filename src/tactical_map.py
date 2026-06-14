"""Mapa táctico 2D para visualización de robots y balón."""

from __future__ import annotations

import cv2
import numpy as np
import pandas as pd

from src.ghost_replay import BGR_COLORS, draw_ghost_replay


def draw_field(width: int = 800, height: int = 500) -> np.ndarray:
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    canvas[:] = (35, 110, 35)

    line_color = (230, 230, 230)
    cv2.rectangle(canvas, (20, 20), (width - 20, height - 20), line_color, 2)
    cv2.line(canvas, (20, height // 2), (width - 20, height // 2), line_color, 2)
    cv2.circle(canvas, (width // 2, height // 2), 55, line_color, 2)

    # Porterías aproximadas
    cv2.rectangle(canvas, (width // 2 - 70, 0), (width // 2 + 70, 20), (0, 220, 255), -1)
    cv2.rectangle(canvas, (width // 2 - 70, height - 20), (width // 2 + 70, height), (255, 120, 40), -1)

    return canvas


def draw_objects_on_map(
    map_img: np.ndarray,
    frame_tracks: pd.DataFrame,
    x_col: str = "x_map",
    y_col: str = "y_map",
) -> np.ndarray:
    scene = map_img.copy()

    if frame_tracks.empty:
        return scene

    for _, row in frame_tracks.iterrows():
        if pd.isna(row.get(x_col)) or pd.isna(row.get(y_col)):
            continue

        x = int(round(row[x_col]))
        y = int(round(row[y_col]))
        team = str(row.get("team", "unknown")).lower()
        color = str(row.get("color", "unknown")).lower()
        class_name = str(row.get("class_name", "")).lower()

        if "ball" in class_name or team == "ball" or color == "orange":
            bgr = BGR_COLORS["ball"]
            radius = 7
        else:
            bgr = BGR_COLORS.get(team, BGR_COLORS.get(color, BGR_COLORS["unknown"]))
            radius = 11

        cv2.circle(scene, (x, y), radius, bgr, -1)
        cv2.circle(scene, (x, y), radius + 2, (255, 255, 255), 1)

        tid = row.get("tracker_id", "?")
        cv2.putText(scene, str(tid), (x + 10, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    return scene


def draw_tactical_map_frame(
    tracks: pd.DataFrame,
    current_frame: int,
    width: int = 800,
    height: int = 500,
    memory: int = 20,
) -> np.ndarray:
    field = draw_field(width, height)
    if not {"x_map", "y_map"}.issubset(tracks.columns):
        return field

    ghost = draw_ghost_replay(field, tracks, current_frame=current_frame, memory=memory, x_col="x_map", y_col="y_map")
    frame_tracks = tracks[tracks["frame"] == current_frame]
    return draw_objects_on_map(ghost, frame_tracks)
