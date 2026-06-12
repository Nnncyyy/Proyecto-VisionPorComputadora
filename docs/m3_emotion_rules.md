# M3 — Reglas de emociones tácticas

Estas emociones no representan emociones humanas reales. Son interpretaciones tácticas calculadas con reglas simples.

## Métricas

| Métrica | Fuente | Uso |
|---|---|---|
| Intensidad | Velocidad del balón y robots | Detectar ritmo del partido |
| Tensión | Distancia del balón a portería | Detectar peligro ofensivo |
| Caos | Robots cerca del balón | Detectar acumulación o presión |
| Dominio | Equipo más cercano al balón | Estimar control del juego |

## Estados

| Estado | Regla aproximada |
|---|---|
| CALMA | Baja intensidad, baja tensión, bajo caos |
| ACTIVO | Movimiento moderado |
| INTENSO | Alta velocidad del balón o robots |
| TENSION | Balón cerca de portería |
| CAOS | Muchos robots alrededor del balón |

## Archivos generados

```text
outputs/metrics/emotions.csv
```
