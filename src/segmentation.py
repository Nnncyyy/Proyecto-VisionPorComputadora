import numpy as np
import supervision as sv
from ultralytics.models.sam import SAM3SemanticPredictor


PROMPTS = [
    {
        "prompt": "robot",
        "class_name": "robot",
        "class_id": 0,
    },
    {
        "prompt": "ball",
        "class_name": "ball",
        "class_id": 1,
    },
]


def load_sam3_text_predictor(model_path: str = "models/sam3.pt", conf: float = 0.25):
    predictor = SAM3SemanticPredictor(
        overrides=dict(
            conf=conf,
            task="segment",
            mode="predict",
            model=model_path,
            verbose=False,
        )
    )
    return predictor


def segment_frame_with_prompts(
    predictor,
    frame,
    prompts: list[dict] = PROMPTS,
) -> sv.Detections:
    """
    Segmenta un frame usando prompts de texto de SAM 3.

    Regresa un objeto sv.Detections combinado con class_id y class_name.
    """
    predictor.set_image(frame)

    all_detections = []

    for item in prompts:
        prompt = item["prompt"]
        class_id = item["class_id"]
        class_name = item["class_name"]

        result = predictor(text=[prompt])[0]
        detections = sv.Detections.from_ultralytics(result)

        if len(detections) == 0:
            continue

        detections.class_id = np.full(len(detections), class_id)

        if detections.confidence is None:
            detections.confidence = np.ones(len(detections))

        detections.data["class_name"] = np.array(
            [class_name] * len(detections)
        )

        all_detections.append(detections)

    if len(all_detections) == 0:
        return sv.Detections.empty()

    return sv.Detections.merge(all_detections)