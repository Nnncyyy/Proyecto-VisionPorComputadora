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

# Milestone 2: Tracking Hallazgo

* M2-01: el video se procesa frame por frame.
* M2-02: hay tracking con IDs.
* M2-03: existe CSV de trayectorias.
* M2-04: hay imagen o video con trails.
* M2-05: hay documentación de errores.