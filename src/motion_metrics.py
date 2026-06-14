"""Métricas de movimiento para tracking, Ghost Replay y emociones tácticas."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def load_tracks_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el CSV de trayectorias: {path}")
    return pd.read_csv(path)


def ensure_tracking_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "team" not in df.columns:
        df["team"] = "unknown"
    if "color" not in df.columns:
        df["color"] = "unknown"
    if "color_score" not in df.columns:
        df["color_score"] = 0.0

    return df


def add_motion_metrics(df: pd.DataFrame, fps: float | None = None) -> pd.DataFrame:
    """
    Agrega vx, vy, speed y direction_change.

    speed queda en px/frame. Si se entrega fps, también agrega speed_px_s.
    """
    df = ensure_tracking_columns(df)
    df = df.copy().sort_values(["tracker_id", "frame"])

    for col in ["vx", "vy", "speed", "direction", "direction_change"]:
        df[col] = 0.0

    groups = df.groupby("tracker_id", sort=False)

    for _, group in groups:
        idx = group.index
        dx = group["x_center"].diff().fillna(0.0)
        dy = group["y_center"].diff().fillna(0.0)
        dframe = group["frame"].diff().replace(0, np.nan).fillna(1.0)

        vx = dx / dframe
        vy = dy / dframe
        speed = np.sqrt(vx**2 + vy**2)
        direction = np.arctan2(vy, vx)
        direction_change = direction.diff().fillna(0.0).abs()
        direction_change = np.minimum(direction_change, 2 * np.pi - direction_change)

        df.loc[idx, "vx"] = vx.values
        df.loc[idx, "vy"] = vy.values
        df.loc[idx, "speed"] = speed.values
        df.loc[idx, "direction"] = direction.values
        df.loc[idx, "direction_change"] = direction_change.values

    if fps is not None:
        df["speed_px_s"] = df["speed"] * float(fps)

    return df.sort_values(["frame", "tracker_id"]).reset_index(drop=True)


def save_motion_tracks(
    input_csv: str | Path,
    output_csv: str | Path,
    fps: float | None = None,
) -> pd.DataFrame:
    df = load_tracks_csv(input_csv)
    df = add_motion_metrics(df, fps=fps)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    return df
