import cv2
import os
import supervision as sv

def extraer_frames(video_path: str, output_dir: str, num_frames: int = 3, stride: int = 50):
    """
    Extrae una cantidad específica de frames de un video y los guarda.
    
    Args:
        video_path (str): Ruta del video de entrada.
        output_dir (str): Carpeta donde se guardarán los frames.
        num_frames (int): Cantidad máxima de frames a extraer.
        stride (int): Salto de frames (ej. 50 significa 1 de cada 50 frames).
    """
    # Crea los directorios si no existen
    os.makedirs(output_dir, exist_ok=True)
    
    # Usamos el generador de Supervision
    generador = sv.get_video_frames_generator(source_path=video_path, stride=stride)
    
    frames_guardados = 0
    for i, frame in enumerate(generador):
        if frames_guardados >= num_frames:
            break
            
        # Calcular el número de frame real y formatearlo (ej. 0001, 0050)
        num_frame_real = i * stride
        # Si es el frame 0, lo guardamos como 1 para coincidir con tu Issue
        if num_frame_real == 0: num_frame_real = 1 
        
        nombre_archivo = f"frame_{num_frame_real:04d}.jpg"
        ruta_guardado = os.path.join(output_dir, nombre_archivo)
        
        # Guardar la imagen optimizada para que sea ligera
        cv2.imwrite(ruta_guardado, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print(f"✅ Frame guardado en: {ruta_guardado}")
        
        frames_guardados += 1
        
    print(f"\nExtracción completada. Se guardaron {frames_guardados} frames en {output_dir}")