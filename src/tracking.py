import supervision as sv


class FutbotTracker:
    """
    Wrapper simple para usar ByteTrack.

    Intenta usar el paquete moderno `trackers`.
    Si no está disponible, usa sv.ByteTrack como respaldo.
    """

    def __init__(self):
        self.mode = None

        try:
            from trackers import ByteTrackTracker

            self.tracker = ByteTrackTracker()
            self.mode = "trackers"
            print("Usando ByteTrackTracker desde paquete trackers")

        except Exception:
            self.tracker = sv.ByteTrack()
            self.mode = "supervision"
            print("Usando sv.ByteTrack como respaldo")

    def update(self, detections: sv.Detections) -> sv.Detections:
        if len(detections) == 0:
            return detections

        if self.mode == "trackers":
            return self.tracker.update(detections)

        return self.tracker.update_with_detections(detections)