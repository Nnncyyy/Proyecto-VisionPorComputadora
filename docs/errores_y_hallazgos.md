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

## Milestone 2

* **Error 1: Cambio de ID**
  * **Problema:**  Un robot cambia de ID después de una oclusión.
  * **Causa probable:**   El tracker pierde continuidad cuando el robot desaparece parcialmente.
  * **Posible solución:**  Ajustar prompts, confianza o usar post-procesamiento en M3.

* **Error 2: Pérdida del balón**
  * **Problema:**  El balón no aparece en algunos frames.
  * **Causa probable:**  Objeto pequeño, movimiento rápido o baja resolución.
  * **Posible solución:**  Combinar SAM 3 con filtrado por color o detección HSV en M3.

* **Error 3: Confusión entre robots**
  * **Problema:**  SAM 3 segmenta varios robots como una sola región o confunde partes del campo.
  * **Causa probable:**  Robots cercanos, oclusiones o prompt demasiado general.
  * **Posible solución:**  Probar prompts más específicos o segmentación por puntos/bboxes.