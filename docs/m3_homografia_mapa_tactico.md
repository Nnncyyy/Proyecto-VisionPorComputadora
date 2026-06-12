# M3 — Homografía y mapa táctico 2D

## Objetivo

Proyectar posiciones del video a un mapa 2D de la cancha para visualizar trayectorias y actividad táctica.

## Archivo de puntos

Crear un archivo JSON con este formato:

```json
{
  "image_points": [[100, 100], [700, 100], [750, 500], [80, 500]],
  "map_points": [[0, 0], [800, 0], [800, 500], [0, 500]]
}
```

`image_points` debe reemplazarse con las cuatro esquinas reales de la cancha en el video.

## Uso

```bash
python src/main_m3.py \
  --tracks outputs/metrics/tracks.csv \
  --video data/raw/videoInstrucciones.mov \
  --homography-points config/homography_points.json
```

## Salidas esperadas

```text
outputs/metrics/tracks_projected.csv
outputs/figures/m3_tactical_map_sample.jpg
```

## Limitaciones

- La homografía es aproximada.
- Funciona mejor si los objetos están sobre el plano de la cancha.
- Si los puntos manuales están mal, el mapa táctico tendrá distorsión.
