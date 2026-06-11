import csv
from pathlib import Path


def init_tracks_csv(csv_path: str | Path):
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "frame",
            "tracker_id",
            "class_id",
            "class_name",
            "x_center",
            "y_center",
            "width",
            "height",
            "confidence",
        ])


def append_tracks_to_csv(csv_path, frame_idx, detections):
    if len(detections) == 0:
        return

    if detections.tracker_id is None:
        return

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for i in range(len(detections)):
            x1, y1, x2, y2 = detections.xyxy[i]

            x_center = float((x1 + x2) / 2)
            y_center = float((y1 + y2) / 2)
            width = float(x2 - x1)
            height = float(y2 - y1)

            class_id = int(detections.class_id[i]) if detections.class_id is not None else -1

            if "class_name" in detections.data:
                class_name = str(detections.data["class_name"][i])
            else:
                class_name = "unknown"

            confidence = (
                float(detections.confidence[i])
                if detections.confidence is not None
                else 0.0
            )

            writer.writerow([
                frame_idx,
                int(detections.tracker_id[i]),
                class_id,
                class_name,
                x_center,
                y_center,
                width,
                height,
                confidence,
            ])