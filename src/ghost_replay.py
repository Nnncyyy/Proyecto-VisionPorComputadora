"""Ghost Replay: visualización histórica de trayectorias."""

from __future__ import annotations

import cv2
import numpy as np
import pandas as pd


BGR_COLORS = {
    "blue": (255, 120, 40),
    "red": (40, 40, 255),
    "orange": (0, 165, 255),
    "yellow": (0, 220, 255),
    "purple": (180, 70, 180),
    "white": (255, 255, 255),
    "unknown": (200, 200, 200),
    "ball": (0, 165, 255),
}


def _color_for_row(row: pd.Series, emotion_color: str | None = None) -> tuple[int, int, int]:
    if emotion_color:
        return BGR_COLORS.get(emotion_color, BGR_COLORS["white"])

    team = str(row.get("team", "unknown")).lower()
    color = str(row.get("color", "unknown")).lower()
    class_name = str(row.get("class_name", "")).lower()

    if "ball" in class_name or team == "ball" or color == "orange":
        return BGR_COLORS["ball"]
    return BGR_COLORS.get(team, BGR_COLORS.get(color, BGR_COLORS["unknown"]))


def draw_ghost_replay(
    frame: np.ndarray,
    tracks: pd.DataFrame,
    current_frame: int,
    memory: int = 18,
    x_col: str = "x_center",
    y_col: str = "y_center",
    emotion_color: str | None = None,
) -> np.ndarray:
    """Dibuja estelas fantasma hasta current_frame."""
    scene = frame.copy()

    if tracks.empty:
        return scene

    start_frame = current_frame - memory
    visible = tracks[(tracks["frame"] >= start_frame) & (tracks["frame"] <= current_frame)].copy()

    if visible.empty:
        return scene

    overlay = scene.copy()

    for tracker_id, obj_df in visible.groupby("tracker_id"):
        obj_df = obj_df.sort_values("frame")
        points = []

        for _, row in obj_df.iterrows():
            if pd.isna(row.get(x_col)) or pd.isna(row.get(y_col)):
                continue
            points.append((int(round(row[x_col])), int(round(row[y_col])), row))

        if not points:
            continue

        # línea para balón o trayectorias rápidas
        last_row = points[-1][2]
        color = _color_for_row(last_row, emotion_color=emotion_color)
        is_ball = str(last_row.get("class_name", "")).lower() == "ball" or str(last_row.get("team", "")).lower() == "ball"

        if len(points) >= 2:
            pts = np.array([[x, y] for x, y, _ in points], dtype=np.int32)
            thickness = 3 if is_ball else 2
            cv2.polylines(overlay, [pts], isClosed=False, color=color, thickness=thickness)

        # círculos con mayor intensidad en posiciones recientes
        n = len(points)
        for idx, (x, y, row) in enumerate(points):
            alpha_weight = (idx + 1) / max(n, 1)
            radius = int(3 + 5 * alpha_weight) if not is_ball else int(2 + 4 * alpha_weight)
            cv2.circle(overlay, (x, y), radius, color, -1)

        # posición actual más visible
        x, y, _ = points[-1]
        cv2.circle(overlay, (x, y), 9 if not is_ball else 7, color, 2)

    cv2.addWeighted(overlay, 0.65, scene, 0.35, 0, dst=scene)
    return scene


def draw_smart_ghost_replay(
    frame: np.ndarray,
    tracks: pd.DataFrame,
    current_frame: int,
    base_memory: int = 14,
    emotion_memory: int | None = None,
    x_col: str = "x_center",
    y_col: str = "y_center",
    emotion_color: str | None = None,
) -> np.ndarray:
    """Ghost Replay con memoria ajustable por emoción."""
    memory = emotion_memory if emotion_memory is not None else base_memory
    return draw_ghost_replay(
        frame=frame,
        tracks=tracks,
        current_frame=current_frame,
        memory=memory,
        x_col=x_col,
        y_col=y_col,
        emotion_color=emotion_color,
    )
