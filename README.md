# Proyecto - Vision Por Computadora
Objetivo: Creación de un proyecto para la Copa FutBotMX con la rama de Visión por Computadora usando SAM 3 (Segment Anything Model 3) de Meta para analizar videos de partidos de fútbol robótico proporcionados por la Federación Mexicana de Robótica.

**Categoría:** Amateur

**Título:** Echomain

**Propuesta de Proyecto:** Sistema de análisis táctico basado en SAM 3 que segmenta, rastrea e interpreta el comportamiento dinámico de un partido de fútbol robótico mediante emociones tácticas y visualización histórica de trayectorias.

**Principales características:** 
- Interpreta emociones tácticas,
- Y visualiza ecos históricos del partido mediante Ghost Replay.

---

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

---

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

---

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

---

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

---

## Avance M3 — HSV, Ghost Replay, emociones tácticas y mapa táctico 2D

En el Milestone 3 convertimos el tracking obtenido en M2 en una visualización narrativa del partido. El objetivo fue que el sistema no solo mostrara robots y balón en movimiento, sino que también interpretara el estado táctico del juego mediante reglas simples y visualizaciones expresivas.

El M3 integra:

```text
Clasificación HSV
Ghost Replay
Memoria emocional
Colores emocionales
Eventos simples
Homografía
Mapa táctico 2D
Mapa de calor
Dashboard narrativo
Visualización combinada
```

---

### Arquitectura del M3

```text
tracks.csv + video original
        ↓
Clasificación HSV
        ↓
Métricas de movimiento
        ↓
Motor de emociones tácticas
        ↓
Ghost Replay
        ↓
Eventos simples
        ↓
Homografía / mapa táctico 2D
        ↓
Dashboard narrativo
        ↓
Video final M3
```

---

### Componentes implementados

| Componente               | Descripción                                            | Evidencia                                                     |
| ------------------------ | ------------------------------------------------------ | ------------------------------------------------------------- |
| HSV                      | Clasificación de color para balón y objetos detectados | `docs/assets/m3/hsv/hsv_sample.jpg`                           |
| CSV enriquecido          | Tracks con color, equipo y score                       | `docs/assets/m3/csv/sample_tracks_m3_metrics.csv`             |
| Ghost Replay básico      | Estelas de posiciones pasadas                          | `docs/assets/m3/ghost_replay/ghost_basic_sample.jpg`          |
| Ghost Replay inteligente | Estelas influenciadas por movimiento/estado táctico    | `docs/assets/m3/ghost_replay/ghost_smart_sample.jpg`          |
| Emociones tácticas       | Estados como CALMA, TENSION y CAOS                     | `docs/assets/m3/events/sample_emotions.csv`                   |
| Colores emocionales      | Trails y dashboard cambian según el estado             | `docs/assets/m3/emotional_colors/emotional_colors_sample.jpg` |
| Memoria emocional        | Longitud del Ghost Replay según el estado              | `docs/assets/m3/emotional_memory/memory_sample.jpg`           |
| Eventos simples          | Detección aproximada de momentos tácticos              | `docs/assets/m3/events/sample_events.csv`                     |
| Homografía               | Proyección del video al mapa 2D                        | `docs/assets/m3/homography/homography_points.jpg`             |
| Mapa táctico 2D          | Visualización superior del partido                     | `docs/assets/m3/tactical_map/tactical_map_sample.jpg`         |
| Mapa de calor            | Zonas de mayor actividad                               | `docs/assets/m3/heatmap/heatmap_sample.jpg`                   |
| Dashboard narrativo      | Estado, intensidad, tensión, caos y evento             | `docs/assets/m3/dashboard/dashboard_sample.jpg`               |
| Visualización narrativa  | Resultado combinado del M3                             | `docs/assets/m3/narrative/m3_narrative_sample.jpg`            |

---

### Evidencias principales

#### Clasificación HSV

![Evidencia HSV](docs/assets/m3/hsv/hsv_sample.jpg)

HSV se utilizó para estimar el color dominante de las detecciones. Funcionó especialmente bien para identificar el balón naranja, aunque presentó confusiones en algunos robots debido a reflejos, LEDs o componentes internos.

#### Ghost Replay

![Ghost Replay](docs/assets/m3/ghost_replay/ghost_basic_sample.jpg)

El Ghost Replay permite visualizar posiciones pasadas de robots y balón, generando una memoria visual del movimiento.

#### Colores emocionales y memoria emocional

![Colores emocionales](docs/assets/m3/emotional_colors/emotional_colors_sample.png)

Los trails cambian de color según el estado táctico del partido. En estados como `CAOS` o `TENSION`, las estelas se vuelven más marcadas para comunicar visualmente la intensidad del momento.

#### Homografía y mapa táctico 2D

![Mapa táctico 2D](docs/assets/m3/tactical_map/tactical_map_sample.jpg)

La homografía permite proyectar las posiciones del video original hacia una cancha 2D. Esta visualización funciona como apoyo táctico y no como medición exacta.

#### Dashboard narrativo

![Dashboard narrativo](docs/assets/m3/dashboard/dashboard_sample.jpg)

El dashboard muestra el estado táctico del partido, intensidad, tensión, caos, dominio y eventos aproximados.

#### Visualización narrativa final

![Visualización narrativa M3](docs/assets/m3/narrative/m3_narrative_sample.png)

La salida final combina video original, Ghost Replay, colores emocionales, dashboard y mapa táctico 2D.

---

### Archivos generados

Durante el M3 se generan archivos locales como:

```text
outputs/metrics/tracks_with_color.csv
outputs/metrics/tracks_projected.csv
outputs/metrics/emotions.csv
outputs/metrics/events.csv
outputs/figures/m3_heatmap_activity.jpg
outputs/videos/m3_narrative_demo.mp4
```

Por tamaño, algunos archivos completos no se suben directamente al repositorio. En su lugar, se incluyen muestras ligeras en:

```text
docs/assets/m3/
```

---

### Cómo ejecutar M3

Primero debe existir el archivo generado en M2:

```text
outputs/metrics/tracks.csv
```

Luego se puede ejecutar M3 sin homografía:

```bash
python src/main_m3.py --tracks outputs/metrics/tracks.csv --video data/raw/videoInstrucciones.mov --max-frames 180
```

Para ejecutar M3 con homografía:

```bash
python src/main_m3.py --tracks outputs/metrics/tracks.csv --video data/raw/videoInstrucciones.mov --homography-points config/homography_points.json --max-frames 180
```

---

### Limitaciones del M3

* HSV funciona bien para el balón naranja, pero puede confundir robots debido a reflejos, luces o componentes internos.
* El dominio puede aparecer como `DOMINIO DESCONOCIDO` porque la clasificación por equipo todavía no es completamente robusta.
* La homografía es una aproximación visual y depende de la correcta selección de los cuatro puntos de la cancha.
* Los eventos detectados son aproximados y se basan en reglas simples.
* Las emociones tácticas no representan emociones humanas reales; son estados visuales calculados con métricas del partido.
* El resultado depende directamente de la calidad del tracking generado en M2.

---

### Estado del Milestone

El M3 queda completado como una primera versión funcional de visualización narrativa. La implementación demuestra que es posible convertir tracking de robots y balón en una experiencia visual con memoria, emociones tácticas, eventos y mapa táctico 2D.

---