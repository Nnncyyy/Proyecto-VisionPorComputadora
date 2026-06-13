# docs/m3_hsv_resultados.md

# M3 — Resultados de clasificación HSV

## Objetivo

El objetivo del módulo HSV fue complementar el tracking y la segmentación del proyecto mediante una clasificación simple de color. Esta clasificación permite estimar si un objeto detectado corresponde a un balón naranja, un robot con color identificable o un objeto desconocido.

HSV no reemplaza a SAM 3 ni al tracking. Su función es servir como herramienta auxiliar para enriquecer los datos y apoyar visualizaciones como dominio, equipos, mapa táctico y dashboard.

---

## Funcionamiento general

El proceso utilizado fue:

```text
Frame del video
    ↓
Detecciones del tracking
    ↓
Bounding box o región del objeto
    ↓
Conversión BGR → HSV
    ↓
Evaluación de rangos de color
    ↓
Asignación de color, equipo y score
```

Las etiquetas generadas fueron:

```text
color
team
color_score
```

Ejemplo:

```text
ball | orange | ball | 0.81
robot | unknown | unknown | 0.01
robot | orange | ball | 0.09
```

---

## Evidencia visual HSV

![Evidencia HSV](assets/m3/hsv/hsv_sample.jpg)

La imagen muestra objetos etiquetados con su clase, color dominante, equipo estimado y puntaje de color.

---

## Resultados obtenidos

El balón naranja fue detectado con mayor claridad que los robots. Esto era esperado, ya que el balón tiene un color más uniforme y contrastante dentro del campo.

En el caso de los robots, la clasificación fue más inestable debido a que algunos contienen luces, cables, reflejos, zonas oscuras y elementos de diferentes colores. Por esta razón, algunos robots fueron clasificados como `orange` o `unknown`.

---

## Hallazgos

* HSV funciona bien para objetos con color uniforme y alto contraste.
* El balón naranja fue el caso más exitoso.
* Algunos robots fueron confundidos como `orange` debido a reflejos o componentes internos.
* La clasificación por equipo todavía requiere ajustes.
* HSV es útil como apoyo visual, pero no debe considerarse una detección perfecta.

---

## Limitaciones

La principal limitación fue la sensibilidad de HSV a iluminación, sombras, reflejos y variación de color dentro de los robots.

Además, en algunos frames los bounding boxes incluyen partes del campo o elementos externos, lo que afecta el cálculo del color dominante.

---

## Decisión para el proyecto

Se decidió mantener HSV como módulo auxiliar del M3, principalmente para:

```text
identificar el balón naranja
enriquecer el CSV
apoyar visualizaciones
documentar experimentación clásica de visión por computadora
```

El cálculo de dominio por equipo queda como una aproximación, ya que la clasificación azul/rojo aún no es completamente robusta.