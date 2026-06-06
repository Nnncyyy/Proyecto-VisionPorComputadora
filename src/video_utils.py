import cv2
import os
from pathlib import Path
import supervision as sv

def get_video_info(video_path: str | Path) -> dict:
    """Obtiene información básica del video (ancho, alto, fps, total_frames)."""
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"No existe el video: {video_path}")

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {video_path}")

    info = {
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "total_frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
    }

    cap.release()
    return info

def iter_video_frames(video_path: str | Path, max_frames: int | None = None, stride: int = 1):
    """Generador eficiente para iterar sobre los frames de un video usando OpenCV nativo."""
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"No existe el video: {video_path}")

    cap = cv2.VideoCapture(str(video_path))
    frame_idx = 0
    yielded = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_idx % stride == 0:
            yield frame_idx, frame
            yielded += 1

        frame_idx += 1

        if max_frames is not None and yielded >= max_frames:
            break

    cap.release()

def create_video_writer(output_path: str | Path, fps: float, width: int, height: int):
    """Crea un objeto VideoWriter para guardar nuevos videos."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    if not writer.isOpened():
        raise RuntimeError(f"No se pudo crear el video de salida: {output_path}")

    return writer

def extraer_frames(video_path: str, output_dir: str, num_frames: int = 3, stride: int = 50):
    """Extrae una cantidad específica de frames y los guarda en el disco utilizando Supervision."""
    os.makedirs(output_dir, exist_ok=True)
    generador = sv.get_video_frames_generator(source_path=video_path, stride=stride)
    
    frames_guardados = 0
    for i, frame in enumerate(generador):
        if frames_guardados >= num_frames:
            break
            
        num_frame_real = i * stride
        if num_frame_real == 0: num_frame_real = 1 
        
        nombre_archivo = f"frame_{num_frame_real:04d}.jpg"
        ruta_guardado = os.path.join(output_dir, nombre_archivo)
        
        cv2.imwrite(ruta_guardado, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print(f"✅ Frame guardado en: {ruta_guardado}")
        
        frames_guardados += 1
        
    print(f"\nExtracción completada. Se guardaron {frames_guardados} frames en {output_dir}")
    
def guardar_frames_procesados(video_path: str | Path, output_dir: str | Path, num_frames: int = 3, stride: int = 50):
    """
    Itera sobre el video y guarda una cantidad específica de frames en el directorio de salida.
    
    Args:
        video_path: Ruta del video original.
        output_dir: Carpeta donde se guardarán los frames extraídos.
        num_frames: Cantidad máxima de frames a salvar.
        stride: Salto entre frames (ej. 50 significa evaluar 1 de cada 50 frames).
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    
    # Crea la carpeta de destino (y sus padres) si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Iniciando extracción nativa en: {output_dir}")
    
    # Usamos tu generador nativo iter_video_frames
    generador = iter_video_frames(video_path, max_frames=num_frames, stride=stride)
    
    frames_guardados = 0
    for frame_idx, frame in generador:
        # Formateamos el nombre (ej. frame_0000.jpg, frame_0050.jpg)
        nombre_archivo = f"frame_{frame_idx:04d}.jpg"
        ruta_guardado = output_dir / nombre_archivo
        
        # Guardamos la imagen con calidad optimizada
        cv2.imwrite(str(ruta_guardado), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print(f"   ✅ Guardado: {nombre_archivo}")
        frames_guardados += 1
        
    print(f"✨ Proceso terminado. Se guardaron {frames_guardados} frames con éxito.\n")