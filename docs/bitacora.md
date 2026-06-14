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

---

## Milestone 3: HSV, Ghost Replay, emociones tácticas y mapa táctico 2D (Junio 2026)

* **Objetivo:** Convertir el tracking obtenido en M2 en una visualización narrativa del partido, integrando clasificación HSV, Ghost Replay, emociones tácticas, eventos simples, homografía, mapa táctico 2D, mapa de calor y dashboard narrativo.
* **Acciones realizadas:**

  * (M3-01) Implementación de un detector HSV para clasificar objetos por color dominante, principalmente balón naranja, robots y objetos desconocidos.
  * (M3-02) Integración de la clasificación HSV al CSV de trayectorias, agregando columnas como `team`, `color` y `color_score`.
  * (M3-03) Implementación de Ghost Replay básico para mostrar posiciones pasadas de robots y balón mediante estelas visuales.
  * (M3-04) Implementación de Ghost Replay inteligente, modificando la longitud y apariencia de las trayectorias según movimiento y estado táctico.
  * (M3-05) Creación de un motor simple de emociones tácticas basado en reglas, usando métricas como intensidad, tensión, caos y dominio.
  * (M3-06) Aplicación de colores emocionales a los trails y al dashboard según estados como `CALMA`, `TENSION` o `CAOS`.
  * (M3-07) Implementación de memoria emocional del Ghost Replay, aumentando la longitud de las estelas en momentos de mayor actividad.
  * (M3-08) Detección de eventos simples del partido, como `posible_tiro`, `posible_colision`, `momento_critico` y `cambio_de_dominio`.
  * (M3-09) Implementación de homografía para proyectar posiciones del video original hacia un mapa táctico 2D.
  * (M3-10) Generación de mapa de calor o zonas de actividad a partir de las posiciones acumuladas de los objetos.
  * (M3-11) Creación de un dashboard narrativo con estado, intensidad, tensión, caos, dominio y evento actual.
  * (M3-12) Creación de una visualización narrativa combinada que integra video original, Ghost Replay, dashboard y mapa táctico 2D.
  * (M3-13) Actualización de documentación y evidencias visuales del M3 en `docs/assets/m3/`.
* **Evidencias generadas:**

  * Evidencia HSV en `docs/assets/m3/hsv/hsv_sample.jpg`.
  * CSV enriquecido en `docs/assets/m3/csv/sample_tracks_m3_metrics.csv`.
  * Ghost Replay básico en `docs/assets/m3/ghost_replay/ghost_basic_sample.jpg`.
  * Ghost Replay inteligente en `docs/assets/m3/ghost_replay/ghost_smart_sample.png`.
  * Colores emocionales en `docs/assets/m3/emotional_colors/emotional_colors_sample.png`.
  * Memoria emocional en `docs/assets/m3/emotional_memory/emotional_memory_sample.png`.
  * Eventos y emociones en `docs/assets/m3/events/`.
  * Mapa de calor en `docs/assets/m3/heatmap/heatmap_sample.jpg`.
  * Homografía en `docs/assets/m3/homography/homography_points.png`.
  * Mapa táctico 2D en `docs/assets/m3/tactical_map/m3_tactical_map_sample.jpg`.
  * Dashboard narrativo en `docs/assets/m3/dashboard/dashboard_sample.jpg`.
  * Visualización narrativa final en `docs/assets/m3/narrative/m3_narrative_sample.png`.
* **Estado:** Completado como primera versión funcional. El M3 logra transformar las trayectorias del M2 en una visualización narrativa con memoria visual, emociones tácticas, eventos simples y mapa táctico 2D.

---

## Milestone 4: Entrega final y reproducibilidad

* **Objetivo:** Preparar el proyecto para entrega final, asegurando que el repositorio pueda instalarse, verificarse y ejecutarse desde cero de forma clara.

* **Acciones realizadas:**
  * (M3-02) Integración de la clasificación HSV al CSV de trayectorias, agregando columnas como `team`, `color` y `color_score`.

  * (M4-01) Crear script principal reproducible
    * Se creó el script `src/run_final_demo.py` para ejecutar el demo final del proyecto desde un solo comando.
    * El script valida la existencia de archivos necesarios como el video original, el archivo `tracks.csv` generado en M2 y el archivo de puntos de homografía.
    * El script ejecuta internamente `src/main_m3.py` para generar la visualización narrativa final.
    * Se agregó soporte para ejecutar el demo con o sin homografía, dependiendo de si existe `config/homography_points.json`.

  * (M4-02) — Revisar instalación y reproducción desde cero**
    * Se revisó el archivo `requirements.txt` para incluir las dependencias principales del proyecto.
    * Se creó el script `src/check_installation.py` para verificar que las librerías principales puedan importarse correctamente.
    * Se probó la instalación del proyecto desde cero siguiendo los pasos documentados.
    * Se verificó que el pipeline pueda reproducirse utilizando los archivos necesarios en las rutas esperadas.
    * Se documentó el proceso de instalación y ejecución en `docs/m4_reproducibilidad.md`.

* **Archivos generados o modificados:**

  * `src/run_final_demo.py`
  * `src/check_installation.py`
  * `requirements.txt`
  * `docs/m4_reproducibilidad.md`
  * `README.md`