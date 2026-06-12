"""Dashboard narrativo sobre video."""

from __future__ import annotations

import cv2
import numpy as np
import pandas as pd


STATE_COLORS = {
    "CALMA": (255, 120, 40),
    "ACTIVO": (0, 220, 255),
    "INTENSO": (0, 140, 255),
    "TENSION": (180, 70, 180),
    "CAOS": (40, 40, 255),
}


def draw_dashboard(
    frame: np.ndarray,
    emotion_row: pd.Series | dict | None = None,
    event_text: str | None = None,
) -> np.ndarray:
    scene = frame.copy()
    h, w = scene.shape[:2]

    x1, y1 = 20, 20
    x2, y2 = min(w - 20, 430), 205

    overlay = scene.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, scene, 0.45, 0, dst=scene)
    cv2.rectangle(scene, (x1, y1), (x2, y2), (255, 255, 255), 1)

    if emotion_row is None:
        emotion_row = {}

    state = str(emotion_row.get("state", "SIN DATOS"))
    color = STATE_COLORS.get(state, (255, 255, 255))

    lines = [
        "ECHOMAIN - Analisis tactico",
        f"Estado: {state}",
        f"Intensidad: {float(emotion_row.get('intensity', 0.0)):.1f}%",
        f"Tension: {float(emotion_row.get('tension', 0.0)):.1f}%",
        f"Caos: {float(emotion_row.get('chaos', 0.0)):.1f}%",
        f"Dominio: {str(emotion_row.get('dominance_label', 'N/A'))}",
    ]

    if event_text:
        lines.append(f"Evento: {event_text[:34]}")

    y = y1 + 28
    for i, text in enumerate(lines):
        text_color = color if i == 1 else (255, 255, 255)
        cv2.putText(scene, text, (x1 + 14, y), cv2.FONT_HERSHEY_SIMPLEX, 0.58, text_color, 2 if i == 1 else 1)
        y += 24

    return scene
