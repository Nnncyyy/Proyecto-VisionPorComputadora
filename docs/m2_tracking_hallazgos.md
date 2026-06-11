# M2 — Tracking funcional

## Objetivo

Rastrear robots y balón a través del video usando las segmentaciones obtenidas con SAM 3 y un tracker basado en ByteTrack.

## Video utilizado

| Campo | Información |
|---|---|
| Nombre local | `videoInstrucciones.mov` |
| Ruta local | `data/raw/videoInstrucciones.mov` |
| Fuente | Repositorio oficial Copa FutBotMX |
| Frames procesados | 100 |
| Stride | 1 |

## Prompts usados

| Clase | Prompt usado | Comentario |
|---|---|---|
| robot | `robot` | Detecta robots, pero puede confundir partes del campo |
| ball | `ball` | El balón puede perderse por tamaño o movimiento |

## Resultados

- Se procesó un fragmento de video frame por frame.
- Se asignaron IDs a objetos detectados.
- Se exportaron trayectorias a CSV.
- Se generó video local con máscaras, cajas, IDs y trails.

## Ejucción
| python -m src.main_m2

## Errores encontrados

### Error 1: Cambio de ID

**Problema:**  
Un robot cambia de ID después de una oclusión.

**Causa probable:**  
El tracker pierde continuidad cuando el robot desaparece parcialmente.

**Posible solución:**  
Ajustar prompts, confianza o usar post-procesamiento en M3.

### Error 2: Pérdida del balón

**Problema:**  
El balón no aparece en algunos frames.

**Causa probable:**  
Objeto pequeño, movimiento rápido o baja resolución.

**Posible solución:**  
Combinar SAM 3 con filtrado por color o detección HSV en M3.

### Error 3: Confusión entre robots

**Problema:**  
SAM 3 segmenta varios robots como una sola región o confunde partes del campo.

**Causa probable:**  
Robots cercanos, oclusiones o prompt demasiado general.

**Posible solución:**  
Probar prompts más específicos o segmentación por puntos/bboxes.

## Decisiones para M3

- Usar el CSV de trayectorias para Ghost Replay.
- Usar posiciones del balón para detectar eventos simples.
- Generar mapa de calor de actividad.

## Avance M2 — Tracking funcional

En este milestone integramos el procesamiento de video frame por frame con un tracker basado en ByteTrack. El objetivo fue asignar IDs persistentes a robots y balón, guardar trayectorias en CSV y generar una primera visualización con máscaras, cajas, IDs y trails.

### Resultados

- Procesamiento frame por frame.
- Segmentación con SAM 3 usando prompts definidos en M1.
- Tracking de objetos con IDs.
- Exportación de trayectorias a CSV.
- Primer video local anotado.

### Evidencia visual

![Tracking sample](docs/runs/segment//image0.jpg)

### Archivos generados localmente

```text
outputs/videos/m2_tracking_demo.mp4
outputs/metrics/tracks.csv