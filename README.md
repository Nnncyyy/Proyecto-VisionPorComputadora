# Proyecto - Vision Por Computadora
Objetivo: Creación de un proyecto para la Copa FutBotMX con la rama de Visión por Computadora usando SAM 3 (Segment Anything Model 3) de Meta para analizar videos de partidos de fútbol robótico proporcionados por la Federación Mexicana de Robótica.

**Categoría:** Amateur

**Título:** Echomain

**Propuesta de Proyecto:** Sistema de análisis táctico basado en SAM 3 que segmenta, rastrea e interpreta el comportamiento dinámico de un partido de fútbol robótico mediante emociones tácticas y visualización histórica de trayectorias.

**Principales características:** 
- Interpreta emociones tácticas,
- Y visualiza ecos históricos del partido mediante Ghost Replay.

## Arquitectura Inicial
El pipeline de procesamiento se compone de las siguientes etapas:
1. **Segmentación Baseline:** Uso del modelo SAM 3 para extraer máscaras precisas de los robots, el balón y los límites del campo.
2. **Tracking (Rastreo):** Implementación de ByteTrack para asignar y mantener identificadores únicos a cada elemento a través del tiempo.
3. **Análisis y Visualización:** Procesamiento de trayectorias para dibujar mapas de calor, Ghost Replays y registrar eventos tácticos en pantalla.

## Avance M1 — Segmentación baseline

En este milestone probamos el modelo SAM 3 sobre frames representativos de partidos de fútbol robótico.

### Objetivos Completados
- Extracción de frames de prueba resguardando el peso del repositorio.
- Pruebas cruzadas de prompts (texto, punto, bounding box).
- Generación de máscaras baseline mediante un módulo reutilizable.
- Documentación técnica de la respuesta del modelo en entornos controlados.

### Evidencia Visual
<img src="docs/assets/m1/baseline/baseline_frame_0050.jpg" alt="Baseline SAM 3" width="48%">
<img src="docs/assets/m1/baseline/baseline_frame_0100.jpg" alt="Baseline SAM 3" width="48%">

### Hallazgos Clave
- **El Balón:** Fue segmentado exitosamente sin requerir preprocesamiento complejo, lo cual es una gran ventaja para la extracción de métricas.
- **Ambigüedad Semántica:** El modelo asocia "player" tanto a los robots como a la audiencia humana.
- **Limitaciones de Entorno:** El prompt "field" falló en detectar el campo de juego, requiriendo métodos tradicionales (polígonos) para delimitar la cancha.
- **Decisión para M2:** Abandonaremos la inferencia pura por texto (*Zero-Shot*). El Milestone 2 utilizará segmentación guiada por *Bounding Boxes* conectadas a algoritmos de Tracking.


## M2 — Tracking funcional
### Objetivo
Rastrear robots y balón a través del video usando las segmentaciones obtenidas con SAM 3 y un tracker basado en ByteTrack.

### Avance M2
En este milestone integramos el procesamiento de video frame por frame con un tracker basado en ByteTrack. El objetivo fue asignar IDs persistentes a robots y balón, guardar trayectorias en CSV y generar una primera visualización con máscaras, cajas, IDs y trails.

### Resultados
- Procesamiento frame por frame.
- Segmentación con SAM 3 usando prompts definidos en M1.
- Tracking de objetos con IDs.
- Exportación de trayectorias a CSV.
- Primer video local anotado.

### Evidencia visual

<img src="https://github.com/Nnncyyy/Proyecto-VisionPorComputadora/blob/m2/runs/segment/predict/image0.jpg?raw=true"  width="48%">
(Es dinámico y se genera cuando se ejecuta el archivo main_m2)

> *Los detalles técnicos se encuentran en [Bitácora](docs/bitacora.md) y en [Registro de Errores y Hallazgos](docs/errores_y_hallazgos.md).*



## Requisitos e Instalación

**Hardware sugerido:** El procesamiento local ha sido probado en equipos con procesadores AMD Ryzen 5 5625U con Radeon Graphics. Para modelos como SAM 3, se recomienda un entorno con aceleración o paciencia en el procesamiento por CPU.

**Instrucciones:**
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/Nnncyyy/Proyecto-VisionPorComputadora.git](https://github.com/Nnncyyy/Proyecto-VisionPorComputadora.git)
   cd Proyecto-VisionPorComputadora

2. Crea un entorno virtual e instala las dependencias:
    ```bash
    pip install -r requirements.txt

3. Descarga el modelo sam3.pt desde HuggingFace y colócalo en la carpeta assets/ (nota: este archivo está ignorado en Git por su tamaño).

> **Nota:** El modelo `sam3.pt` debe descargarse desde Hugging Face y colocarse en la carpeta `assets/`, ya que ha sido excluido de GitHub mediante el archivo `.gitignore` debido a su gran tamaño.


## Integrantes
- Nancy Ashanti Del Castillo Aguirre
- Diego Garcia Mendoza

## M3 — HSV, Homografía, Ghost Replay y emociones tácticas

### Objetivo
Convertir las trayectorias generadas en M2 en una visualización narrativa del partido. En este milestone se agregan clasificación por color mediante HSV, métricas de movimiento, emociones tácticas, eventos simples, Ghost Replay, mapa de calor, homografía opcional y dashboard.

### Componentes de M3
- **HSV:** clasifica objetos como robot azul, robot rojo, balón naranja o desconocido.
- **Ghost Replay:** dibuja posiciones pasadas como estelas o ecos del movimiento.
- **Emociones tácticas:** calcula estados como `CALMA`, `ACTIVO`, `INTENSO`, `TENSION` y `CAOS` con reglas explicables.
- **Homografía / mapa táctico 2D:** proyecta posiciones a una vista superior de la cancha si se definen puntos manuales.
- **Eventos simples:** detecta posibles colisiones, tiros o cambios de dominio.
- **Dashboard:** muestra intensidad, tensión, caos, dominio y evento actual sobre el video.

### Ejecutar M3 sin homografía

Primero ejecuta M2 para generar:

```text
outputs/metrics/tracks.csv
```

Después corre:

```bash
python src/main_m3.py \
  --tracks outputs/metrics/tracks.csv \
  --video data/raw/videoInstrucciones.mov \
  --max-frames 180
```

### Ejecutar M3 con homografía

Copia la plantilla:

```text
config/homography_points_template.json
```

y guárdala como:

```text
config/homography_points.json
```

Edita `image_points` con las cuatro esquinas reales de la cancha en el video. Luego ejecuta:

```bash
python src/main_m3.py \
  --tracks outputs/metrics/tracks.csv \
  --video data/raw/videoInstrucciones.mov \
  --homography-points config/homography_points.json \
  --max-frames 180
```

### Salidas locales esperadas

```text
outputs/metrics/tracks_with_color.csv
outputs/metrics/tracks_projected.csv
outputs/metrics/emotions.csv
outputs/metrics/events.csv
outputs/figures/m3_heatmap_activity.jpg
outputs/figures/m3_tactical_map_sample.jpg
outputs/videos/m3_narrative_demo.mp4
```

Estos archivos se generan localmente y no se suben completos al repositorio por tamaño. Solo se subirán evidencias ligeras en `docs/assets/m3/`.

### Limitaciones actuales
- HSV puede fallar con sombras, reflejos o iluminación variable.
- Las emociones tácticas son reglas simples, no emociones humanas reales.
- Los eventos son aproximados.
- La homografía depende de puntos manuales bien elegidos.
