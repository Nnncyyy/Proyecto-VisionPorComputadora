import numpy as np
from ultralytics.models.sam import SAM3SemanticPredictor
import supervision as sv

def load_text_prompt_predictor(model_path: str, conf: float = 0.25):
    """
    Carga el modelo SAM 3 optimizado para ejecución en CPU, 
    listo para recibir prompts de texto (Zero-Shot).
    """
    predictor = SAM3SemanticPredictor(
        overrides=dict(
            conf=conf,
            task="segment",
            mode="predict",
            model=model_path,
            verbose=False,
            device="cpu"  # Forzamos CPU por estabilidad
        )
    )
    return predictor

def segment_with_text_prompt(predictor, image: np.ndarray, prompt: str) -> sv.Detections:
    """
    Extrae máscaras de una imagen usando un texto descriptivo y
    devuelve las detecciones en el formato universal de Supervision.
    """
    predictor.set_image(image)
    result = predictor(text=[prompt])[0]
    
    # Conversión al formato unificado
    detections = sv.Detections.from_ultralytics(result)
    return detections