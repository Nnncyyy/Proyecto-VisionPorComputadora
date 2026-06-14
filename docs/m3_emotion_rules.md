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

Colores emocionales

Se definieron colores visuales para reforzar la narrativa:

CALMA → azul
ACTIVO → amarillo
TENSION → naranja
CAOS → rojo
MOMENTO CRÍTICO → rojo / morado

Estos colores se aplican en trails, dashboard y visualización narrativa.

Memoria emocional

La longitud del Ghost Replay cambia según el estado táctico:

CALMA → memoria corta
ACTIVO → memoria media
TENSION → memoria media/larga
CAOS → memoria larga

Esto permite que el espectador perciba visualmente la intensidad del momento.

Eventos simples

Los eventos detectados son aproximados y se basan en reglas:

posible_tiro
posible_colision
momento_critico
cambio_de_dominio

No se consideran eventos oficiales del partido, sino indicadores visuales para enriquecer la narrativa.

Limitaciones

El motor emocional depende directamente de la calidad del tracking. Si el tracking pierde objetos, cambia IDs o detecta falsos positivos, las métricas pueden variar.

También depende de la homografía y la clasificación HSV, por lo que algunos valores como dominio pueden ser incompletos.

## Archivos generados

```text
outputs/metrics/emotions.csv
```
