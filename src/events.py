"""Detección aproximada de eventos tácticos."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.emotion_engine import split_ball_and_robots


def _point_cols(df: pd.DataFrame) -> tuple[str, str]:
    if {"x_map", "y_map"}.issubset(df.columns) and df[["x_map", "y_map"]].notna().any().all():
        return "x_map", "y_map"
    return "x_center", "y_center"


def detect_events(
    tracks: pd.DataFrame,
    emotions: pd.DataFrame | None = None,
    collision_distance: float = 45.0,
    shot_speed: float = 30.0,
    tension_threshold: float = 65.0,
) -> pd.DataFrame:
    """Genera eventos simples a partir de trayectorias y emociones."""
    if tracks.empty:
        return pd.DataFrame(columns=["frame", "event", "description"])

    x_col, y_col = _point_cols(tracks)
    emotions_by_frame = {}
    if emotions is not None and not emotions.empty:
        emotions_by_frame = emotions.set_index("frame").to_dict(orient="index")

    rows = []
    last_dominant_team = None

    for frame, frame_df in tracks.groupby("frame"):
        balls, robots = split_ball_and_robots(frame_df)
        emotion = emotions_by_frame.get(frame, {})

        # Colisiones aproximadas entre robots
        if len(robots) >= 2:
            robot_rows = list(robots.iterrows())
            for i in range(len(robot_rows)):
                idx_a, a = robot_rows[i]
                for j in range(i + 1, len(robot_rows)):
                    idx_b, b = robot_rows[j]
                    dist = float(np.hypot(float(a[x_col]) - float(b[x_col]), float(a[y_col]) - float(b[y_col])))
                    if dist <= collision_distance:
                        rows.append({
                            "frame": int(frame),
                            "event": "posible_colision",
                            "description": f"Robots {a.get('tracker_id')} y {b.get('tracker_id')} cerca ({dist:.1f}px)",
                        })

        # Tiro aproximado: balón rápido + tensión alta
        if not balls.empty:
            ball = balls.sort_values("speed", ascending=False).iloc[0]
            ball_speed = float(ball.get("speed", 0.0))
            tension = float(emotion.get("tension", 0.0))
            if ball_speed >= shot_speed and tension >= tension_threshold:
                rows.append({
                    "frame": int(frame),
                    "event": "posible_tiro",
                    "description": f"Balón rápido ({ball_speed:.1f}px/frame) con tensión {tension:.1f}%",
                })

        dominant_team = emotion.get("dominant_team")
        if dominant_team and dominant_team != "unknown":
            if last_dominant_team is not None and dominant_team != last_dominant_team:
                rows.append({
                    "frame": int(frame),
                    "event": "cambio_de_dominio",
                    "description": f"Dominio cambia de {last_dominant_team} a {dominant_team}",
                })
            last_dominant_team = dominant_team

        state = emotion.get("state")
        if state in {"CAOS", "TENSION"}:
            rows.append({
                "frame": int(frame),
                "event": "momento_critico",
                "description": f"Estado táctico: {state}",
            })

    return pd.DataFrame(rows)


def save_events(
    tracks_csv: str | Path,
    emotions_csv: str | Path | None,
    output_csv: str | Path,
    **kwargs,
) -> pd.DataFrame:
    tracks = pd.read_csv(tracks_csv)
    emotions = pd.read_csv(emotions_csv) if emotions_csv and Path(emotions_csv).exists() else None
    events = detect_events(tracks, emotions, **kwargs)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(output_csv, index=False)
    return events
