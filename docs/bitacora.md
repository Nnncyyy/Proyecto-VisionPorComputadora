# Bitácora del Proyecto

## Milestone 0: Repositorio Listo
* **Objetivo:** Configurar la base del proyecto y las reglas de control de versiones.
* **Acciones realizadas:**
  * Creación del repositorio en GitHub.
  * Configuración del archivo `.gitignore` para proteger el repositorio de archivos pesados (videos y modelos de 3GB).
  * Definición de la estructura de carpetas (`src`, `docs`, `data`, `notebooks`).
  * Creación del archivo `requirements.txt` con las librerías base (Supervision, Ultralytics, OpenCV).

## Milestone 1: Segmentación Baseline con SAM 3 (Mayo 2026)
* **Objetivo:** Probar SAM 3 sobre frames estáticos y obtener primeras máscaras.
* **Acciones realizadas:**
  * (M1-01) Extracción de frames representativos en `docs/assets/m1/frames/`.
  * (M1-02) Validación de carga de SAM 3 con procesamiento local en CPU para garantizar estabilidad sin CUDA.
  * (M1-03 y M1-04) Pruebas de prompts (Texto vs Punto vs BBox). Se documentó el sesgo de clases del dataset COCO (YOLO) y se determinó que BBox es el método de mayor precisión.
  * (M1-05) Creación del pipeline base estructurado en `src/segmentation.py`.
  * (M1-06 y M1-07) Registro de hallazgos finales: imposibilidad de segmentar la cancha con "field", ambigüedad del término "player" y éxito total con el balón.
* **Estado:** Completado.

---

## Milestone 2: Tracking funcional

* **Objetivo:** Rastrear robots y balón a través del video mediante IDs persistentes y trayectorias exportables.
* **Acciones realizadas:**
  * (M2-01) Se creó un pipeline de video frame por frame usando `src/main_m2.py`.
  * (M2-02) Se integró `FutbotTracker` como wrapper de ByteTrack en `src/tracking.py`.
  * (M2-03) Se creó exportación de trayectorias a CSV mediante `src/export.py`.
  * (M2-04) Se generó visualización con máscaras, cajas, IDs y trails usando `src/visualization.py`.
  * (M2-05) Se documentaron errores y hallazgos en `docs/m2_tracking_hallazgos.md` y `docs/errores_y_hallazgos.md`.
  * Se agregó el notebook `notebooks/06_tracking_basico.ipynb` para validar el tracking de forma reproducible.
  * Se agregó evidencia ligera en `docs/assets/m2/`.

* **Estado:** En cierre / validado con evidencia ligera.