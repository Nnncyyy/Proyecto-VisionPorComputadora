"""
Pipeline M3 — HSV, Homografía, Ghost Replay, emociones tácticas y dashboard.

Este script parte del CSV generado en M2. No ejecuta SAM 3; usa las trayectorias
para construir la capa narrativa del proyecto.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import pandas as pd

# Permite ejecutar: python src/main_m3.py desde la raíz del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.color_utils import classify_tracks_with_hsv
from src.dashboard import draw_dashboard
from src.emotion_engine import color_name_for_state, compute_emotions, memory_length_for_state
from src.events import detect_events
from src.ghost_replay import draw_smart_ghost_replay
from src.heatmap import create_heatmap_image
from src.homography import compute_homography, load_homography_points, project_tracks_to_map
from src.motion_metrics import add_motion_metrics
from src.tactical_map import draw_tactical_map_frame
from src.video_utils import create_video_writer, get_video_info


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline M3 de Echomain")

    parser.add_argument(
        "--tracks",
        type=Path,
        default=PROJECT_ROOT / "outputs" / "metrics" / "tracks.csv",
        help="CSV generado en M2.",
    )
    parser.add_argument(
        "--video",
        type=Path,
        default=None,
        help="Video original. Necesario para HSV y video narrativo.",
    )
    parser.add_argument(
        "--homography-points",
        type=Path,
        default=None,
        help="JSON con puntos de homografía. Opcional.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "outputs",
        help="Carpeta base de salida.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=180,
        help="Número máximo de frames para generar video narrativo.",
    )
    parser.add_argument(
        "--skip-video",
        action="store_true",
        help="Solo genera CSVs, mapa táctico y mapas de calor; no genera video.",
    )

    return parser.parse_args()


def select_event_for_frame(events: pd.DataFrame, frame_idx: int) -> str | None:
    if events.empty:
        return None
    frame_events = events[events["frame"] == frame_idx]
    if frame_events.empty:
        return None
    return str(frame_events.iloc[0].get("event", ""))


def get_emotion_for_frame(emotions: pd.DataFrame, frame_idx: int) -> dict:
    if emotions.empty:
        return {}
    frame_rows = emotions[emotions["frame"] == frame_idx]
    if frame_rows.empty:
        # Usar última emoción conocida para que el dashboard no desaparezca.
        previous = emotions[emotions["frame"] <= frame_idx]
        if previous.empty:
            return {}
        return previous.iloc[-1].to_dict()
    return frame_rows.iloc[0].to_dict()


def generate_narrative_video(
    video_path: Path,
    tracks: pd.DataFrame,
    emotions: pd.DataFrame,
    events: pd.DataFrame,
    output_video: Path,
    max_frames: int = 180,
    include_tactical_map: bool = False,
) -> None:
    info = get_video_info(video_path)
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {video_path}")

    video_width = info["width"]
    video_height = info["height"]
    map_panel_width = 480 if include_tactical_map else 0
    output_width = video_width + map_panel_width
    output_height = video_height

    writer = create_video_writer(
        output_path=output_video,
        fps=info["fps"],
        width=output_width,
        height=output_height,
    )

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx > max_frames:
            break

        emotion = get_emotion_for_frame(emotions, frame_idx)
        state = str(emotion.get("state", "CALMA"))
        memory = memory_length_for_state(state)
        emotion_color = color_name_for_state(state)

        scene = draw_smart_ghost_replay(
            frame=frame,
            tracks=tracks,
            current_frame=frame_idx,
            emotion_memory=memory,
            emotion_color=emotion_color,
        )

        event_text = select_event_for_frame(events, frame_idx)
        scene = draw_dashboard(scene, emotion_row=emotion, event_text=event_text)

        if include_tactical_map:
            tactical = draw_tactical_map_frame(tracks, frame_idx, width=800, height=500, memory=memory)
            tactical = cv2.resize(tactical, (map_panel_width, output_height))
            scene = cv2.hconcat([scene, tactical])

        writer.write(scene)
        frame_idx += 1

    cap.release()
    writer.release()


def main() -> None:
    args = parse_args()

    metrics_dir = args.output_dir / "metrics"
    figures_dir = args.output_dir / "figures"
    videos_dir = args.output_dir / "videos"

    metrics_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    videos_dir.mkdir(parents=True, exist_ok=True)

    if not args.tracks.exists():
        raise FileNotFoundError(
            f"No existe {args.tracks}. Primero ejecuta M2 para generar tracks.csv."
        )

    print(f"Leyendo trayectorias: {args.tracks}")
    tracks = pd.read_csv(args.tracks)

    # M3-01 y M3-02: HSV, si hay video disponible.
    hsv_csv = metrics_dir / "tracks_with_color.csv"
    if args.video is not None and args.video.exists():
        print("Aplicando HSV para clasificar color/equipo...")
        tracks = classify_tracks_with_hsv(args.video, args.tracks, hsv_csv, max_frames=args.max_frames)
    else:
        print("No se proporcionó video; se omite HSV y se usan etiquetas existentes.")
        if "team" not in tracks.columns:
            tracks["team"] = "unknown"
        if "color" not in tracks.columns:
            tracks["color"] = "unknown"
        if "color_score" not in tracks.columns:
            tracks["color_score"] = 0.0
        tracks.to_csv(hsv_csv, index=False)

    # Métricas de movimiento.
    print("Calculando métricas de movimiento...")
    tracks = add_motion_metrics(tracks)

    # M3-09: Homografía opcional.
    include_tactical_map = False
    projected_csv = metrics_dir / "tracks_projected.csv"
    if args.homography_points is not None and args.homography_points.exists():
        print("Aplicando homografía...")
        image_points, map_points = load_homography_points(args.homography_points)
        H = compute_homography(image_points, map_points)
        tracks = project_tracks_to_map(tracks, H)
        include_tactical_map = True
    else:
        print("No se proporcionaron puntos de homografía; se omite mapa táctico proyectado.")

    tracks.to_csv(projected_csv, index=False)
    print(f"CSV M3 guardado: {projected_csv}")

    # M3-05: emociones tácticas.
    print("Calculando emociones tácticas...")
    emotions = compute_emotions(tracks)
    emotions_csv = metrics_dir / "emotions.csv"
    emotions.to_csv(emotions_csv, index=False)
    print(f"Emociones guardadas: {emotions_csv}")

    # M3-08: eventos.
    print("Detectando eventos simples...")
    events = detect_events(tracks, emotions)
    events_csv = metrics_dir / "events.csv"
    events.to_csv(events_csv, index=False)
    print(f"Eventos guardados: {events_csv}")

    # M3-10: mapa de calor.
    print("Generando mapa de calor...")
    heatmap_path = figures_dir / "m3_heatmap_activity.jpg"
    create_heatmap_image(tracks, heatmap_path)
    print(f"Mapa de calor guardado: {heatmap_path}")

    # M3-09: muestra de mapa táctico si hay homografía.
    if include_tactical_map and not tracks.empty:
        sample_frame = int(tracks["frame"].min())
        tactical = draw_tactical_map_frame(tracks, sample_frame)
        tactical_path = figures_dir / "m3_tactical_map_sample.jpg"
        cv2.imwrite(str(tactical_path), tactical)
        print(f"Mapa táctico guardado: {tactical_path}")

    # M3-11: video narrativo.
    if not args.skip_video and args.video is not None and args.video.exists():
        output_video = videos_dir / "m3_narrative_demo.mp4"
        print("Generando video narrativo M3...")
        generate_narrative_video(
            video_path=args.video,
            tracks=tracks,
            emotions=emotions,
            events=events,
            output_video=output_video,
            max_frames=args.max_frames,
            include_tactical_map=include_tactical_map,
        )
        print(f"Video narrativo guardado: {output_video}")
    else:
        print("Video narrativo omitido. Usa --video para generarlo.")

    print("M3 completado a nivel de código base.")


if __name__ == "__main__":
    main()
