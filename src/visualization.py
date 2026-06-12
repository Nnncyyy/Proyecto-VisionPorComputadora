import cv2
import supervision as sv


mask_annotator = sv.MaskAnnotator(opacity=0.45)
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()


def draw_tracking_frame(frame, detections):
    """
    Dibuja máscaras, cajas, IDs y trayectorias.
    """
    scene = frame.copy()

    if len(detections) == 0:
        return scene

    scene = mask_annotator.annotate(scene=scene, detections=detections)
    scene = box_annotator.annotate(scene=scene, detections=detections)

    labels = []

    for i in range(len(detections)):
        if detections.tracker_id is not None:
            tid = detections.tracker_id[i]
        else:
            tid = "?"

        if "class_name" in detections.data:
            class_name = detections.data["class_name"][i]
        else:
            class_name = "obj"

        labels.append(f"{class_name} #{tid}")

    scene = label_annotator.annotate(
        scene=scene,
        detections=detections,
        labels=labels,
    )

    if detections.tracker_id is not None:
        scene = trace_annotator.annotate(
            scene=scene,
            detections=detections,
        )

    return scene