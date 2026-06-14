from pathlib import Path
import argparse
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_VIDEO = PROJECT_ROOT / "data" / "raw" / "videoInstrucciones.mov"
DEFAULT_TRACKS = PROJECT_ROOT / "outputs" / "metrics" / "tracks.csv"
DEFAULT_HOMOGRAPHY = PROJECT_ROOT / "config" / "homography_points.json"
MAIN_M3 = PROJECT_ROOT / "src" / "main_m3.py"


def check_file(path: Path, required: bool = True) -> bool:
    if path.exists():
        print(f"[OK] {path.relative_to(PROJECT_ROOT)}")
        return True

    if required:
        print(f"[ERROR] No se encontró: {path.relative_to(PROJECT_ROOT)}")
    else:
        print(f"[AVISO] No se encontró: {path.relative_to(PROJECT_ROOT)}")

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta el demo final de Echomain usando el pipeline M3."
    )

    parser.add_argument(
        "--video",
        type=Path,
        default=DEFAULT_VIDEO,
        help="Ruta del video original.",
    )

    parser.add_argument(
        "--tracks",
        type=Path,
        default=DEFAULT_TRACKS,
        help="Ruta del CSV de trayectorias generado en M2.",
    )

    parser.add_argument(
        "--homography-points",
        type=Path,
        default=DEFAULT_HOMOGRAPHY,
        help="Ruta del archivo de puntos de homografía.",
    )

    parser.add_argument(
        "--max-frames",
        type=int,
        default=180,
        help="Número máximo de frames para procesar.",
    )

    parser.add_argument(
        "--no-homography",
        action="store_true",
        help="Ejecuta M3 sin homografía.",
    )

    args = parser.parse_args()

    video_path = args.video if args.video.is_absolute() else PROJECT_ROOT / args.video
    tracks_path = args.tracks if args.tracks.is_absolute() else PROJECT_ROOT / args.tracks
    homography_path = (
        args.homography_points
        if args.homography_points.is_absolute()
        else PROJECT_ROOT / args.homography_points
    )

    print("ECHOMAIN — Demo final")
    print("Verificando archivos necesarios...")

    if not check_file(video_path, required=True):
        print("\nColoca el video en data/raw/videoInstrucciones.mov o usa --video.")
        sys.exit(1)

    if not check_file(tracks_path, required=True):
        print("\nPrimero genera el tracking con:")
        print("python src/main_m2.py")
        sys.exit(1)

    check_file(MAIN_M3, required=True)

    cmd = [
        sys.executable,
        str(MAIN_M3),
        "--tracks",
        str(tracks_path),
        "--video",
        str(video_path),
        "--max-frames",
        str(args.max_frames),
    ]

    if not args.no_homography and homography_path.exists():
        cmd.extend(["--homography-points", str(homography_path)])
    else:
        print("[AVISO] Ejecutando sin homografía.")

    print("\nEjecutando comando:")
    print(" ".join(cmd))

    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)

    print("\nDemo final generado:")
    print("outputs/videos/m3_narrative_demo.mp4")


if __name__ == "__main__":
    main()