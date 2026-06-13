# Registro de Errores y Hallazgos

Este documento centraliza los problemas técnicos encontrados, los descubrimientos sobre el comportamiento de los modelos (SAM 3, YOLO, ByteTrack) y las decisiones arquitectónicas tomadas a lo largo del proyecto Copa FutBotMX.

---

## Plantilla de Registro (Cómo documentar)
Para cada nueva entrada, utilizar el siguiente formato:
* **[Tipo: Error | Hallazgo | Decisión] - Título breve**
  * **Contexto:** (En qué issue, notebook o script ocurrió)
  * **Descripción:** (Qué sucedió, qué intentaban hacer o qué comportamiento notaron en el modelo)
  * **Solución / Impacto:** (Cómo se resolvió el error o qué camino se decidió tomar a partir de este hallazgo)

---

## Milestone 1: Segmentación Baseline con SAM 3

* **[Hallazgo] - Tiempos de carga y ejecución en procesador**
  * **Contexto:** Issue M1-02 (Verificar carga de SAM 3).
  * **Descripción:** Al ejecutar inferencia en un entorno local sin aceleración de GPU dedicada (usando un procesador AMD Ryzen), el modelo SAM 3 toma un tiempo considerable tanto en la carga en memoria como en la generación de máscaras.
  * **Solución / Impacto:** Se debe forzar el parámetro `device="cpu"` en la inicialización del modelo para evitar crashes. La carga inicial de SAM 3 toma alrededor de 30 segundos ejecutándose en CPU.

* **[Hallazgo] - Falsos positivos con prompts de texto**
  * **Contexto:** Issue M1-03 (Pruebas de prompts de texto con SAM 3).
  * **Descripción:** Al intentar aislar elementos usando descripciones generales en inglés (como "ball" o "robot"), SAM 3 logra segmentarlos, con prompts como "player" suele incluir tambien a las personas además de los robots.

* **[Hallazgo] - El modelo base de YOLO detecta humanos, no robots**
  * **Contexto:** Issue M1-04 (Pruebas de Bounding Boxes combinadas con YOLOv8n).
  * **Descripción:** Al intentar usar YOLOv8n sin re-entrenar para obtener las coordenadas de un robot, el modelo detectó a una persona del público en el fondo. Esto ocurre porque en el dataset COCO por defecto de YOLO, la clase 0 corresponde a "person". SAM 3 segmentó a la persona perfectamente usando esa caja.
  * **Solución / Impacto:** La prueba validó que el método de *Bounding Box* es el más preciso para SAM 3. Sin embargo, nos advierte que para el Milestone 2 (Tracking), no podremos usar YOLOv8n directamente desde la caja. Tendremos que usar un detector basado en color (HSV) para los robots y el balón, o entrenar un modelo YOLO personalizado.

* **[Decisión] - Implementación estricta del Baseline de Segmentación por Texto**
  * **Contexto:** Issue M1-05 (Generar segmentación baseline).
  * **Descripción:** Se construyó el módulo reutilizable `src/segmentation.py` exportando las funciones requeridas para segmentar por texto (`load_text_prompt_predictor` y `segment_with_text_prompt`).
  * **Solución / Impacto:** Aunque en el Issue M1-04 determinamos que las *Bounding Boxes* ofrecen mayor precisión técnica para nuestro proyecto, se establece este código como nuestro *Baseline* (Punto de referencia) para cumplir con el entregable inicial. Para el Milestone 2, este módulo será escalado agregando una función `segment_with_bbox` que consumirá las cajas fuertes entregadas por nuestro sistema de Tracking o detección por color.

* **[Hallazgo] - Oclusiones y ruido en la detección del balón**
  * **Contexto:** Issue M1-06 (Reflexión final de segmentación).
  * **Descripción:** Durante las pruebas, notamos que los robots parcialmente ocultos (oclusiones, donde un robot tapa a otro) son difíciles de segmentar completos con prompts de texto; la máscara suele cortarse. Uno de los elementos que no se pudieron segmentar fue el campo, no pudiendo segmentar el espacio del juego.
  * **Solución / Impacto:** Para el Milestone 2, el balón requerirá filtrado estricto por color (HSV) para garantizar una Bounding Box precisa. Estas cajas delimitadoras ayudarán a resolver las oclusiones aislando cada elemento antes de pasarlo a SAM 3.
---

* **[Hallazgo] - Falla en la segmentación del campo ("field")**
  * **Contexto:** Issue M1-06 (Reflexión final de segmentación).
  * **Descripción:** Al intentar segmentar la cancha usando el prompt de texto "field", el modelo SAM 3 falló por completo y no generó ninguna máscara. Es probable que la textura verde uniforme y la iluminación no ofrezcan suficientes contrastes para que el modelo identifique los bordes semánticos de un "campo".
  * **Solución / Impacto:** Se descarta el uso de prompts de texto para aislar la cancha. Para necesidades futuras (como mapas de calor), deberemos definir el área de juego estáticamente usando polígonos manuales o algoritmos de detección de bordes (Canny) sobre las líneas blancas.

* **[Hallazgo] - Ambigüedad semántica en prompts ("player")**
  * **Contexto:** Issue M1-06 (Pruebas de precisión).
  * **Descripción:** Se observó que el modelo es altamente sensible a la semántica del prompt. Al usar la palabra "player", SAM 3 no diferenció entre los robots de la competencia y el público humano en el fondo, segmentando a ambos grupos simultáneamente.
  * **Solución / Impacto:** Confirma la necesidad de abandonar los prompts genéricos de texto para la etapa de Tracking. Reafirma nuestra decisión de usar *Bounding Boxes* generadas por un detector propio para garantizar que solo se segmenten los robots en la cancha.

* **[Hallazgo Positivo] - Éxito en la detección del balón**
  * **Contexto:** Issue M1-06 (Pruebas de precisión).
  * **Descripción:** Contrario a nuestras hipótesis iniciales, el balón fue capturado y segmentado de manera correcta sin presentar problemas graves de confusión con el fondo al usar SAM 3.
  * **Impacto:** Esto facilita el desarrollo del Milestone 2, ya que podremos confiar en la máscara generada para el balón sin requerir filtros de posprocesamiento tan estrictos.

---

## Milestone 2:


---

## Milestone 3: HSV, Ghost Replay, emociones tácticas y mapa táctico 2D

* **[Hallazgo] - HSV funciona mejor para el balón que para los robots**

  * **Contexto:** Issue M3-01 (Implementar detector HSV para robots y balón).
  * **Descripción:** Al aplicar HSV sobre las detecciones, el balón naranja fue identificado con mayor claridad que los robots. En algunos frames, ciertos robots fueron clasificados como `orange` o `ball`.
  * **Causa probable:** Los robots contienen LEDs, cables, reflejos y componentes internos con colores similares al naranja. Además, algunos bounding boxes incluyen zonas del campo o partes externas al robot.
  * **Solución / Impacto:** Se mantuvo HSV como herramienta auxiliar y se agregó `color_score` para interpretar la confianza de la clasificación. Se documentó que HSV es útil para el balón, pero limitado para distinguir equipos de forma robusta.

* **[Hallazgo] - El dominio puede aparecer como desconocido**

  * **Contexto:** Issue M3-05 (Crear motor simple de emociones tácticas).
  * **Descripción:** En algunos frames, el dashboard muestra `DOMINIO DESCONOCIDO`.
  * **Causa probable:** La clasificación por equipo todavía no distingue de forma confiable entre robots azules y rojos usando únicamente HSV.
  * **Solución / Impacto:** Se decidió conservar la etiqueta `DOMINIO DESCONOCIDO` cuando no existe suficiente evidencia de color. Esto evita forzar una clasificación incorrecta y mantiene el sistema honesto respecto a sus limitaciones.

* **[Hallazgo] - La homografía depende mucho de los cuatro puntos seleccionados**

  * **Contexto:** Issue M3-09 (Implementar homografía y mapa táctico 2D).
  * **Descripción:** Al inicio, algunos puntos proyectados quedaban fuera del mapa táctico 2D.
  * **Causa probable:** Los puntos de referencia estaban mal ordenados, eran aproximados o no correspondían exactamente con las esquinas de la cancha.
  * **Solución / Impacto:** Se corrigió la selección manual de los cuatro puntos de la cancha y se documentó que la homografía funciona como una aproximación visual, no como una medición exacta.

* **[Hallazgo] - El mapa táctico 2D tiene fondo estático**

  * **Contexto:** Issue M3-09 y M3-12 (Mapa táctico 2D y visualización narrativa combinada).
  * **Descripción:** El mapa táctico de la derecha permanece visualmente fijo durante el video.
  * **Causa probable:** Esto es esperado, ya que la cancha 2D funciona como un fondo canónico estático. Lo que debe cambiar son los puntos y trayectorias proyectadas sobre ese fondo.
  * **Solución / Impacto:** Se verificó que los objetos proyectados aparezcan cuando existen datos de tracking para esos frames. Se documentó que el mapa táctico es una visualización de apoyo sobre un campo fijo.

* **[Hallazgo] - Los eventos simples son aproximaciones narrativas**

  * **Contexto:** Issue M3-08 (Detectar eventos simples del partido).
  * **Descripción:** Eventos como `posible_tiro`, `posible_colision` o `momento_critico` pueden activarse sin que necesariamente exista un evento oficial del partido.
  * **Causa probable:** Las reglas usan métricas simples como velocidad, distancia, tensión o cercanía entre objetos.
  * **Solución / Impacto:** Se documentó que los eventos son indicadores narrativos aproximados. Para categoría Amateur, se priorizó que las reglas fueran simples, explicables y visualmente útiles.

* **[Hallazgo] - Ghost Replay ayuda a interpretar el movimiento**

  * **Contexto:** Issues M3-03, M3-04 y M3-07 (Ghost Replay básico, inteligente y memoria emocional).
  * **Descripción:** Las estelas visuales permiten observar el historial reciente de robots y balón, haciendo más claro el movimiento dentro del partido.
  * **Resultado positivo:** El Ghost Replay se convirtió en uno de los elementos visuales más fuertes del proyecto, ya que transforma coordenadas de tracking en una experiencia visual entendible.
  * **Solución / Impacto:** Se mantuvo como componente central de la visualización narrativa y se conectó con colores emocionales y memoria variable.

* **[Hallazgo] - La memoria emocional hace más expresivos los momentos de caos**

  * **Contexto:** Issue M3-07 (Implementar memoria emocional del Ghost Replay).
  * **Descripción:** En estados como `CAOS` o `TENSION`, las trayectorias largas ayudan a comunicar mayor actividad visual.
  * **Resultado positivo:** La longitud de las estelas refuerza la idea de que el partido tiene momentos de calma, tensión o caos.
  * **Solución / Impacto:** Se definió una regla visual donde `CALMA` usa memoria corta, `ACTIVO` memoria media y `CAOS` memoria larga.

* **[Hallazgo] - El dashboard mejora la narrativa del video**

  * **Contexto:** Issue M3-11 (Crear dashboard narrativo).
  * **Descripción:** El dashboard permite mostrar en pantalla el estado actual del partido, incluyendo intensidad, tensión, caos, dominio y evento.
  * **Resultado positivo:** La visualización deja de ser solo técnica y empieza a contar una historia del partido.
  * **Solución / Impacto:** Se integró el dashboard en la visualización final del M3 junto con Ghost Replay y mapa táctico 2D.

* **[Hallazgo] - El resultado depende directamente de la calidad del tracking de M2**

  * **Contexto:** Relación entre M2 y M3.
  * **Descripción:** Si el tracking pierde objetos, cambia IDs o genera falsos positivos, las emociones, eventos, Ghost Replay y mapa táctico también se ven afectados.
  * **Causa probable:** El M3 utiliza `tracks.csv` como entrada principal, por lo que cualquier error del M2 se propaga.
  * **Solución / Impacto:** Se documentó esta dependencia y se mantuvieron las visualizaciones como aproximaciones interpretativas, no como mediciones perfectas.
