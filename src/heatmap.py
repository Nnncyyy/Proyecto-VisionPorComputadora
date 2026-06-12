"""Mapas de calor de actividad."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pandas as pd


def create_heatmap_image(
    tracks: pd.DataFrame,
    output_path: str | Path,
    class_filter: str | None = None,
    team_filter: str | None = None,
    width: int = 800,
    height: int = 500,
) -> np.ndarray:
    df = tracks.copy()

    if class_filter is not None and "class_name" in df.columns:
        df = df[df["class_name"].astype(str).str.lower() == class_filter.lower()]

    if team_filter is not None and "team" in df.columns:
        df = df[df["team"].astype(str).str.lower() == team_filter.lower()]

    x_col, y_col = ("x_map", "y_map") if {"x_map", "y_map"}.issubset(df.columns) else ("x_center", "y_center")

    heat = np.zeros((height, width), dtype=np.float32)

    if not df.empty:
        xs = df[x_col].astype(float).clip(0, width - 1).astype(int)
        ys = df[y_col].astype(float).clip(0, height - 1).astype(int)
        for x, y in zip(xs, ys):
            cv2.circle(heat, (int(x), int(y)), 16, 1.0, -1)

    heat = cv2.GaussianBlur(heat, (0, 0), sigmaX=18, sigmaY=18)

    if heat.max() > 0:
        heat_norm = np.uint8(np.clip(heat / heat.max() * 255, 0, 255))
    else:
        heat_norm = np.zeros_like(heat, dtype=np.uint8)

    heat_color = cv2.applyColorMap(heat_norm, cv2.COLORMAP_JET)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), heat_color)
    return heat_color
