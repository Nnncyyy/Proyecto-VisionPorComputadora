# M3 — Resultados HSV

## Objetivo

Clasificar objetos rastreados como `blue`, `red`, `orange` o `unknown` usando HSV sobre la región de cada bounding box.

## Uso esperado

```bash
python src/main_m3.py --tracks outputs/metrics/tracks.csv --video data/raw/videoInstrucciones.mov --max-frames 180
```

## Salidas esperadas

```text
outputs/metrics/tracks_with_color.csv
```

Columnas nuevas:

```text
team,color,color_score
```

## Limitaciones

- HSV depende mucho de iluminación, sombras y reflejos.
- Si el robot tiene poco color visible, puede quedar como `unknown`.
- El balón puede confundirse con marcas naranjas o reflejos.
- HSV se usa como apoyo visual/táctico, no como detector perfecto.
