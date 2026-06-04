# Pruebas de prompts SAM 3 — M1

| Prompt | Frame | Resultado | Problema |
|---|---|---|---|
| robot | frame_0050 | Detecta varios robots en la cancha. | - |
| ball | frame_0050 | Detecta el balón de manera correcta. | Podría detectar otros círculos falsos en la imagen o manchas en el campo. |
| soccer robot | frame_0001 | Detecta los robots de la cancha | Detecta mejor los robots al estar más separados. |
| player | frame_0100 | Identifica los jugadores. | Identifica también a las personas como jugadores. |
| person | frame_0050 | Aísla a las personas de los robots. | - |

## Comparativa de Métodos de Prompt (M1-04)

Al ejecutar la comparativa visual entre Texto, Punto y Bounding Box (BBox) sobre el `frame_0050.jpg`, obtuvimos un comportamiento inesperado pero muy revelador sobre los modelos pre-entrenados:

* **Prompt de Texto ("robot"):** SAM 3 logró identificar a los 3 robots sobre la cancha y los segmentó al mismo tiempo. Es útil para una vista general, pero no permite aislar a un solo robot de forma individual.
* **Prompt de Punto y Bounding Box (con YOLOv8n):** Utilizamos un modelo YOLO estándar para intentar automatizar la obtención de la coordenada y la caja. Sin embargo, YOLOv8 está entrenado con el dataset COCO, donde la clase 0 es "Persona". Por lo tanto, ignoró a los robots, detectó a un espectador en el fondo de la imagen y le pasó esa caja/punto a SAM 3. 
* **Comportamiento de SAM 3:** A pesar del "error" de YOLO, SAM 3 demostró su potencia. Al recibir la BBox del espectador, generó un recorte perfecto, limpio y sin ruido del fondo.

### Decisiones Arquitectónicas para M2
1.  **El método ganador es la Bounding Box:** Queda demostrado que encerrar el objeto en una caja le da a SAM 3 los límites exactos que necesita para no mezclar la máscara con el entorno.
2.  **Reemplazo del detector:** No podremos usar el modelo genérico de YOLO para rastrear el partido. Para el Milestone 2, desarrollaremos un detector basado en máscaras de color (HSV) o implementaremos un modelo entrenado específicamente para nuestros robots y balón. Esas detecciones generarán las cajas que alimentarán a SAM 3.