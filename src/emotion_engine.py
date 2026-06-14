"""Motor de emociones tácticas basado en reglas simples y explicables."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


BALL_NAMES = {"ball", "balon", "balón"}


def _is_ball_row(row: pd.Series) -> bool:
    class_name = str(row.get("class_name", "")).lower()
    team = str(row.get("team", "")).lower()
    color = str(row.get("color", "")).lower()
    return any(name in class_name for name in BALL_NAMES) or team == "ball" or color == "orange"


def split_ball_and_robots(frame_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if frame_df.empty:
        return frame_df.copy(), frame_df.copy()
    mask_ball = frame_df.apply(_is_ball_row, axis=1)
    return frame_df[mask_ball].copy(), frame_df[~mask_ball].copy()


def _point_cols(df: pd.DataFrame) -> tuple[str, str]:
    """Usa coordenadas de mapa si existen; si no, coordenadas del video."""
    if {"x_map", "y_map"}.issubset(df.columns) and df[["x_map", "y_map"]].notna().any().all():
        return "x_map", "y_map"
    return "x_center", "y_center"


def nearest_team_to_ball(ball: pd.Series, robots: pd.DataFrame, x_col: str, y_col: str) -> tuple[str, float]:
    if robots.empty:
        return "unknown", float("inf")

    dx = robots[x_col].astype(float) - float(ball[x_col])
    dy = robots[y_col].astype(float) - float(ball[y_col])
    distances = np.sqrt(dx**2 + dy**2)
    nearest_idx = distances.idxmin()
    team = str(robots.loc[nearest_idx].get("team", "unknown"))
    return team, float(distances.loc[nearest_idx])


def classify_state(intensity: float, tension: float, chaos: float) -> str:
    if chaos >= 70:
        return "CAOS"
    if tension >= 70:
        return "TENSION"
    if intensity >= 70:
        return "INTENSO"
    if intensity >= 35:
        return "ACTIVO"
    return "CALMA"


def compute_emotions(
    tracks: pd.DataFrame,
    goal_top: tuple[float, float] | None = None,
    goal_bottom: tuple[float, float] | None = None,
    chaos_radius: float = 120.0,
    intensity_scale: float = 35.0,
) -> pd.DataFrame:
    """Calcula intensidad, tensión, caos, dominio y estado por frame."""
    if tracks.empty:
        return pd.DataFrame()

    df = tracks.copy()
    if "speed" not in df.columns:
        df["speed"] = 0.0
    if "team" not in df.columns:
        df["team"] = "unknown"

    x_col, y_col = _point_cols(df)

    if goal_top is None:
        goal_top = (float(df[x_col].max() / 2), float(df[y_col].min()))
    if goal_bottom is None:
        goal_bottom = (float(df[x_col].max() / 2), float(df[y_col].max()))

    max_dist = max(
        float(np.hypot(df[x_col].max() - df[x_col].min(), df[y_col].max() - df[y_col].min())),
        1.0,
    )

    rows = []

    for frame, frame_df in df.groupby("frame"):
        balls, robots = split_ball_and_robots(frame_df)

        ball_speed = float(balls["speed"].max()) if not balls.empty else 0.0
        robot_speed = float(robots["speed"].mean()) if not robots.empty else 0.0
        raw_intensity = ball_speed * 0.65 + robot_speed * 0.35
        intensity = float(np.clip((raw_intensity / intensity_scale) * 100, 0, 100))

        tension = 0.0
        chaos = 0.0
        dominant_team = "unknown"
        nearest_distance = float("inf")

        if not balls.empty:
            ball = balls.iloc[0]
            ball_xy = np.array([float(ball[x_col]), float(ball[y_col])])

            dist_top = np.linalg.norm(ball_xy - np.array(goal_top))
            dist_bottom = np.linalg.norm(ball_xy - np.array(goal_bottom))
            tension = float(np.clip((1.0 - min(dist_top, dist_bottom) / max_dist) * 100, 0, 100))

            if not robots.empty:
                dx = robots[x_col].astype(float) - ball_xy[0]
                dy = robots[y_col].astype(float) - ball_xy[1]
                distances = np.sqrt(dx**2 + dy**2)
                robots_near = int((distances <= chaos_radius).sum())
                chaos = float(np.clip((robots_near / max(len(robots), 1)) * 100, 0, 100))
                dominant_team, nearest_distance = nearest_team_to_ball(ball, robots, x_col, y_col)

        state = classify_state(intensity, tension, chaos)

        if dominant_team in {"blue", "red"}:
            dominance_label = f"DOMINIO {dominant_team.upper()}"
        else:
            dominance_label = "DOMINIO DESCONOCIDO"

        rows.append({
            "frame": int(frame),
            "intensity": round(intensity, 2),
            "tension": round(tension, 2),
            "chaos": round(chaos, 2),
            "state": state,
            "dominant_team": dominant_team,
            "dominance_label": dominance_label,
            "nearest_robot_distance": round(nearest_distance, 2) if np.isfinite(nearest_distance) else None,
        })

    return pd.DataFrame(rows)


def save_emotions(
    tracks_csv: str | Path,
    output_csv: str | Path,
    **kwargs,
) -> pd.DataFrame:
    tracks = pd.read_csv(tracks_csv)
    emotions = compute_emotions(tracks, **kwargs)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    emotions.to_csv(output_csv, index=False)
    return emotions


def memory_length_for_state(state: str) -> int:
    """Cantidad de frames pasados que debe recordar Ghost Replay."""
    state = str(state).upper()
    if state == "CALMA":
        return 8
    if state == "ACTIVO":
        return 16
    if state == "INTENSO":
        return 24
    if state == "TENSION":
        return 28
    if state == "CAOS":
        return 36
    return 14


def color_name_for_state(state: str) -> str:
    state = str(state).upper()
    if state == "CALMA":
        return "blue"
    if state == "ACTIVO":
        return "yellow"
    if state == "INTENSO":
        return "orange"
    if state == "TENSION":
        return "purple"
    if state == "CAOS":
        return "red"
    return "white"
